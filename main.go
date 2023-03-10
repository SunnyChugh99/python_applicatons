/*
Copyright 2018 The Kubernetes Authors.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"io/ioutil"
	v1 "k8s.io/api/admission/v1"
	"k8s.io/api/admission/v1beta1"
	"k8s.io/apimachinery/pkg/runtime"
	"k8s.io/klog"
	"net/http"
	"os"
	// TODO: try this library to see if it generates correct json patch
	// https://github.com/mattbaird/jsonpatch
)

var (
	certFile     string
	keyFile      string
	port         int
	sidecarImage string
	injectorType string
)

func init() {
	flag.StringVar(&certFile, "tls-cert-file", "",
		"File containing the default x509 Certificate for HTTPS. (CA cert, if any, concatenated after server cert).")
	flag.StringVar(&keyFile, "tls-private-key-file", "",
		"File containing the default x509 private key matching --tls-cert-file.")
	flag.IntVar(&port, "port", 443,
		"Secure port that the webhook listens on")
	flag.StringVar(&sidecarImage, "sidecar-image", "",
		"Image to be used as the injected sidecar")

}

// admitv1beta1Func handles a v1beta1 admission
type admitv1beta1Func func(v1beta1.AdmissionReview) *v1beta1.AdmissionResponse

// admitv1beta1Func handles a v1 admission
type admitv1Func func(v1.AdmissionReview) *v1.AdmissionResponse

// admitHandler is a handler, for both validators and mutators, that supports multiple admission review versions
type admitHandler struct {
	v1beta1 admitv1beta1Func
	v1      admitv1Func
}

func newDelegateToV1AdmitHandler(f admitv1Func) admitHandler {
	return admitHandler{
		v1beta1: delegateV1beta1AdmitToV1(f),
		v1:      f,
	}
}

func delegateV1beta1AdmitToV1(f admitv1Func) admitv1beta1Func {
	return func(review v1beta1.AdmissionReview) *v1beta1.AdmissionResponse {
		in := v1.AdmissionReview{Request: convertAdmissionRequestToV1(review.Request)}
		out := f(in)
		return convertAdmissionResponseToV1beta1(out)
	}
}

// serve handles the http portion of a request prior to handing to an admit
// function
func serve(w http.ResponseWriter, r *http.Request, admit admitHandler) {
	var body []byte
	if r.Body != nil {
		if data, err := ioutil.ReadAll(r.Body); err == nil {
			body = data
		}
	}

	injectorType = os.Getenv("injectorType")

	// verify the content type is accurate
	contentType := r.Header.Get("Content-Type")
	if contentType != "application/json" {
		klog.Errorf("contentType=%s, expect application/json", contentType)
		return
	}

	klog.Info(fmt.Sprintf("handling request: %s", body))

	deserializer := codecs.UniversalDeserializer()
	obj, gvk, err := deserializer.Decode(body, nil, nil)
	if err != nil {
		msg := fmt.Sprintf("Request could not be decoded: %v", err)
		klog.Error(msg)
		http.Error(w, msg, http.StatusBadRequest)
		return
	}

	var responseObj runtime.Object
	switch *gvk {
	case v1beta1.SchemeGroupVersion.WithKind("AdmissionReview"):
		requestedAdmissionReview, ok := obj.(*v1beta1.AdmissionReview)
		if !ok {
			klog.Errorf("Expected v1beta1.AdmissionReview but got: %T", obj)
			return
		}
		responseAdmissionReview := &v1beta1.AdmissionReview{}
		responseAdmissionReview.SetGroupVersionKind(*gvk)
		responseAdmissionReview.Response = admit.v1beta1(*requestedAdmissionReview)
		responseAdmissionReview.Response.UID = requestedAdmissionReview.Request.UID
		responseObj = responseAdmissionReview
	case v1.SchemeGroupVersion.WithKind("AdmissionReview"):
		requestedAdmissionReview, ok := obj.(*v1.AdmissionReview)
		if !ok {
			klog.Errorf("Expected v1.AdmissionReview but got: %T", obj)
			return
		}
		responseAdmissionReview := &v1.AdmissionReview{}
		responseAdmissionReview.SetGroupVersionKind(*gvk)
		responseAdmissionReview.Response = admit.v1(*requestedAdmissionReview)
		responseAdmissionReview.Response.UID = requestedAdmissionReview.Request.UID
		responseObj = responseAdmissionReview
	default:
		msg := fmt.Sprintf("Unsupported group version kind: %v", gvk)
		klog.Error(msg)
		http.Error(w, msg, http.StatusBadRequest)
		return
	}

	klog.V(2).Info(fmt.Sprintf("sending response: %v", responseObj))
	respBytes, err := json.Marshal(responseObj)
	if err != nil {
		klog.Error(err)
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	w.Header().Set("Content-Type", "application/json")
	if _, err := w.Write(respBytes); err != nil {
		klog.Error(err)
	}
}

func serveMutatePods(w http.ResponseWriter, r *http.Request) {
	serve(w, r, newDelegateToV1AdmitHandler(mutatePods))
}

func serveMutatePodsSidecar(w http.ResponseWriter, r *http.Request) {
	fmt.Println("---------------------6-------------------")
	serve(w, r, newDelegateToV1AdmitHandler(mutatePodsSidecar))
}

func main() {
	fmt.Println("---------------------1-------------------")
	loggingFlags := &flag.FlagSet{}
	klog.InitFlags(loggingFlags)
	flag.Parse()

	config := Config{
		CertFile: certFile,
		KeyFile:  keyFile,
	}
	fmt.Println("---------------------1-------------------")
	http.HandleFunc("/mutating-pods", serveMutatePods)
	http.HandleFunc("/mutating-pods-sidecar", serveMutatePodsSidecar)
	fmt.Println("---------------------2-------------------")
	http.HandleFunc("/readyz", func(w http.ResponseWriter, req *http.Request) { w.Write([]byte("ok")) })
	fmt.Println("---------------------3-------------------")
	server := &http.Server{
		Addr:      fmt.Sprintf(":%d", port),
		TLSConfig: configTLS(config),
	}
	fmt.Println("---------------------4-------------------")
	err := server.ListenAndServeTLS("", "")
	fmt.Println("---------------------5-------------------")
	if err != nil {

	}

	fmt.Println("---------------------9-------------------")

	var patch string = `[
{"op":"add","path":"/spec/initContainers","value":[{"image":"mosaiccloudacr.azurecr.io/sunny.chugh/sidecar_injector/init-container:handle","name":"secrets-init-container","imagePullPolicy": "Always","volumeMounts":[{"name":"secret-vol","mountPath":"/tmp"},{"name":"app-config","mountPath":"/tmp/mosaic-secret-manager.ini","subPath":"mosaic-secret-manager.ini"}],"env":[{"name": "SECRET_ARN","valueFrom": {"fieldRef":{ {"fieldPath": "metadata.annotations['secrets.k8s.refract/secret-arn']"}}},{"name": "INJECTOR_TYPE","valueFrom": {"secretKeyRef":{{"key":"injector.type"},{"name":"secret-inject-tls-mosaic"}}}},{"name":"SECRET_FILENAME","value":"/tmp/mosaic-automl-backend.ini"}],"resources":{}}]},{"op":"add","path":"/spec/volumes/-","value":{"emptyDir": {"medium": "Memory"},"name": "secret-vol"}},{"op":"add","path":"/spec/volumes/-","value":{"name":"app-config","configMap": {"items": [{"key": "mosaic-secret-manager.ini" , "path": "mosaic-secret-manager.ini" }],"name": "mosaic-automl-backend"}}},{"op": "add","path": "/spec/containers/0/volumeMounts/-","value": {"mountPath":"/mosaic-automl-backend/configs-test/","name": "secret-vol"}}]`

	reviewResponse := v1.AdmissionResponse{}
	fmt.Println("---------------------8-------------------")
	fmt.Println(patch)

	reviewResponse.Patch = []byte(patch)
	fmt.Println("---------------------16-------------------")
	pt := v1.PatchTypeJSONPatch
	reviewResponse.PatchType = &pt
	fmt.Println("---------------------17-------------------")

	fmt.Println("---------------------18-------------------")

	fmt.Println("---------------------18-------------------")
	fmt.Println(reviewResponse.PatchType)
	fmt.Println(pt)
	fmt.Println("---------------------19-------------------")
	fmt.Println(reviewResponse)
	fmt.Println("---------------------20-------------------")

}
