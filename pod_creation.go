package main

import (
	"fmt"
	"strings"
        "strconv"

	"k8s.io/api/admission/v1"
	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/klog"
)


var podsInitContainerPatch string = `[
{"op":"add","path":"/spec/initContainers","value":[{"image":"aa","name":"secrets-init-container","imagePullPolicy": "Always","volumeMounts":[{"name":"secret-vol","mountPath":"/tmp"},{"name":"app-config","mountPath":"/tmp/mosaic-secret-manager.ini","subPath":"mosaic-secret-manager.ini"}],"env":[{"name": "SECRET_ARN","valueFrom": {"fieldRef":{ {"fieldPath": "metadata.annotations['secrets.k8s.refract/secret-arn']"}}},{"name": "INJECTOR_TYPE","valueFrom": {"secretKeyRef":{{"name":"secret-inject-tls-mosaic"},{"key":"injector.type"}}}}`


func hasContainer(containers []corev1.Container, containerName string) bool {
	for _, container := range containers {
		if container.Name == containerName {
			return true
		}
	}
	return false
}


func mutatePods(ar v1.AdmissionReview) *v1.AdmissionResponse {
	fmt.Println("---------------------7-------------------")
	shouldPatchPod := func(pod *corev1.Pod) bool {
                  podsInitContainerPatch  =  `[
{"op":"add","path":"/spec/initContainers","value":[{"image":"%v","name":"secrets-init-container","imagePullPolicy": "Always","volumeMounts":[{"name":"secret-vol","mountPath":"/tmp"},{"name":"app-config","mountPath":"/tmp/mosaic-secret-manager.ini","subPath":"mosaic-secret-manager.ini"}],"env":[{"name": "SECRET_ARN","valueFrom": {"fieldRef":{ {"fieldPath": "metadata.annotations['secrets.k8s.refract/secret-arn']"}}},{"name": "INJECTOR_TYPE","valueFrom": {"secretKeyRef":{{"name":"secret-inject-tls-mosaic"},{"key":"injector.type"}}}}`

               return !hasContainer(pod.Spec.InitContainers, "secrets-init-container")
        }
    fmt.Println("---------------------8-------------------")
    fmt.Println("---------------------9-------------------")
	return applyPodPatch(ar, shouldPatchPod, podsInitContainerPatch)
}

func applyPodPatch(ar v1.AdmissionReview, shouldPatchPod func(*corev1.Pod) bool, patch string) *v1.AdmissionResponse {
	fmt.Println("---------------------10-------------------")
	klog.V(2).Info("mutating pods")
	podResource := metav1.GroupVersionResource{Group: "", Version: "v1", Resource: "pods"}
	if ar.Request.Resource != podResource {
		klog.Errorf("expect resource to be %s", podResource)
		return nil
	}
	fmt.Println("---------------------11-------------------")
	raw := ar.Request.Object.Raw
	pod := corev1.Pod{}
	deserializer := codecs.UniversalDeserializer()
	fmt.Println("---------------------12-------------------")
	if _, _, err := deserializer.Decode(raw, nil, &pod); err != nil {
		klog.Error(err)
		return toV1AdmissionResponse(err)
	}
	reviewResponse := v1.AdmissionResponse{}
	reviewResponse.Allowed = true
	fmt.Println("---------------------13-------------------")
	if shouldPatchPod(&pod) {
                mount_path ,mount_path_ok := pod.ObjectMeta.Annotations["secrets.k8s.refract/mount-path"]
                secret_filename ,secret_filename_ok := pod.ObjectMeta.Annotations["secrets.k8s.refract/secret-filename"]
                configmap_name ,configmap_name_ok := pod.ObjectMeta.Annotations["secrets.k8s.refract/configmap_name"]
                file_name ,file_name_ok := pod.ObjectMeta.Annotations["secrets.k8s.refract/file_name"]

                var path = "{\"op\": \"add\",\"path\": \"/spec/containers/"
                var value = "/volumeMounts/-\",\"value\": {\"mountPath\": \"/tmp/\",\"name\": \"secret-vol\"}}"
                if mount_path_ok == true {
                    value = "/volumeMounts/-\",\"value\": {\"mountPath\":" + "\"" +  mount_path +"\""+ ",\"name\": \"secret-vol\"}}"
                }
                fmt.Println("---------------------14-------------------")
                fmt.Println(configmap_name_ok)
                fmt.Println(file_name_ok)
                fmt.Println(configmap_name)
                fmt.Println(file_name)

                var vol_mounts = ""
                for i, _ := range pod.Spec.Containers {
                    if i == 0  {
                        vol_mounts = path + strconv.Itoa(i) + value
                        } else {
                        vol_mounts = vol_mounts + "," + path + strconv.Itoa(i) + value
                    }
                }

                if secret_filename_ok == true  {
                   patch = patch + ",{\"name\":\"SECRET_FILENAME\",\"value\":"+ "\"" + secret_filename + "\"}"
                }
                if  len(pod.Spec.InitContainers) == 0 {
                    fmt.Println("---------------------15-------------------")
                	fmt.Println("aya init me1 ")
                    // patch = patch + `],"resources":{}}]},{"op":"add","path":"/spec/volumes/-","value":{"emptyDir": {"medium": "Memory"},"name": "secret-vol"}},{"op":"add","path":"/spec/volumes/-","value":{"name":"app-config","configMap": {"items": [{"key": "mosaic-ai-backend.ini" , "path": "mosaic-ai-backend.ini" }],"name": "` + configmap_name + "\"}}}" + "," + vol_mounts + "]"
                       patch = patch + fmt.Sprintf(`],"resources":{}}]},{"op":"add","path":"/spec/volumes/-","value":{"emptyDir": {"medium": "Memory"},"name": "secret-vol"}},{"op":"add","path":"/spec/volumes/-","value":{"name":"app-config","configMap": {"items": [{"key": "%s" , "path": "%s" }],"name": "%s"}}}` + "," + vol_mounts + "]",file_name,file_name,configmap_name)
                 } else  {
                 	fmt.Println("nahi aya init me ")
                 	fmt.Println(patch)
                    // patch = patch + `],"resources":{}}},{"op":"add","path":"/spec/volumes/-","value":{"emptyDir": {"medium": "Memory"},"name": "secret-vol"}},{"op":"add","path":"/spec/volumes/-","value":{"name":"app-config","configMap": {"items": [{"key": "mosaic-ai-backend.ini" , "path": "mosaic-ai-backend.ini" }],"name": "mosaic-ai-backend"}}}` + "," + vol_mounts + "]"
                    patch = patch + fmt.Sprintf(`],"resources":{}}},{"op":"add","path":"/spec/volumes/-","value":{"emptyDir": {"medium": "Memory"},"name": "secret-vol"}},{"op":"add","path":"/spec/volumes/-","value":{"name":"app-config","configMap": {"items": [{"key": "%s" , "path": "%s" }],"name": "%s"}}}` + "," + vol_mounts + "]",file_name,file_name,configmap_name)

                }
		reviewResponse.Patch = []byte(patch)
	    fmt.Println("---------------------16-------------------")
		pt := v1.PatchTypeJSONPatch
		reviewResponse.PatchType = &pt
		fmt.Println("---------------------17-------------------")
                klog.Info(patch)
        fmt.Println("---------------------18-------------------")
	}
//        klog.Info(&reviewResponse)
	return &reviewResponse
}
