from kubernetes import client, config
from datetime import datetime

# Load the Kubernetes configuration file
#config.load_kube_config()
config.load_incluster_config()
# Create a Kubernetes API client
v1 = client.CoreV1Api()

# Define the namespace and event payload
namespace = "refract-dev"
pod_name = 'dp-9dacf3d8-7963-467b-8929-803f47d64242-849969688f-8nkk5'
current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
event_name = f"my-event-{pod_name}-{current_time}"

event_payload = {
    "metadata": {
        "name": event_name,
        "namespace": namespace
    },
    "involvedObject": {
        "kind": "Pod",
        "name": pod_name,
        "namespace": namespace
    },
    "reason": "Testing",
    "message": "This is a test event",
    "type": "Package-installation",
    "lastTimestamp": current_time
}

# Create the event in Kubernetes
try:
    api_response = v1.create_namespaced_event(namespace, event_payload)
    print("Event created. Involved object='%s'" % str(api_response.involved_object.name))
    print(api_response)
except client.rest.ApiException as e:
    print("Exception when calling CoreV1Api->create_namespaced_event: %s\n" % e)
