from kubernetes import client, config, watch
from datetime import datetime as date_time

# Load Kubernetes configuration
config.load_incluster_config()

# Create Kubernetes client
api = client.CoreV1Api()

# Define pod name and namespace
pod_name = "jy-d18ba884-2fb8-4b2b-88dc-9ce48c30d963-refractadmin-16ef4cf4"
namespace = "refract-dev"

# Get pod details
pod = api.read_namespaced_pod(name=pod_name, namespace=namespace)
print(pod.status)



if pod.status.init_container_statuses is not None:
    for container in pod.status.init_container_statuses:
        if container.ready:
            print(f"Container {container.name} is ready")
        else:
            print(f"Container {container.name} is not ready")
else:
    print("No container status found for the pod")


# Check if container has started
if pod.status.container_statuses is not None:
    for container in pod.status.container_statuses:
        if container.ready:
            print(f"Container {container.name} is ready")
        else:
            print(f"Container {container.name} is not ready")
else:
    print("No container status found for the pod")

field_selector = "involvedObject.name=" + pod_name
stream = watch.Watch().stream(api.list_namespaced_event,
                              namespace=namespace,
                              field_selector=field_selector,
                              timeout_seconds=1)

event_list = []
progress = ""
for event in stream:
    field_path = event["object"].involved_object.field_path

    if event["object"].event_time is None:
        progress = event["object"].type + " " + event["object"].message
    else:
        progress = date_time.strftime(event["object"].event_time, "%Y-%m-%d %H:%M:%S") \
                   + " " + event["object"].type + " " + event["object"].message
    if event not in event_list:
        event_list.append(progress)

print(event_list)
print(progress)