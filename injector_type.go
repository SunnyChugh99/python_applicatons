{"op":"add",
"path":"/spec/initContainers/0",
"value":
{"image":"%v","name":"secrets-init-container","imagePullPolicy": "Always","volumeMounts":
[{"name":"secret-vol","mountPath":"/tmp"}],"env":[{"name": "SECRET_ARN","valueFrom": {"fieldRef": {"fieldPath": "metadata.annotations['secrets.k8s.aws/secret-arn']"}}},{"name": "INJECTOR_TYPE","valueFrom": {"fieldRef":
{"fieldPath": "metadata.annotations['secrets.k8s.aws/injector-type']"
}
}
}`
