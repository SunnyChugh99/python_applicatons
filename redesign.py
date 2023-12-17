'''

DEFAULT:
Stage-1 : resource allocation
Stage-2 : git-init
Stage-3 : notebooks
Stage-4 : knights-watch


stage: {
        '1' : {'status':'waiting', 'logs':''}
		'2' : {'status':'waiting', 'logs':''},
		'3' : {'status':'waiting', 'logs':''},
		'4' : {'status':'waiting', 'logs':''}
        }

'''

from kubernetes import client, config, watch
from datetime import datetime as date_time
import os

# Load Kubernetes configuration
config.load_incluster_config()

# Create Kubernetes client
api = client.CoreV1Api()

# Define pod name and namespace
pod_name = "jy-9ac1f53b-8cda-43a1-a670-79fa6427549e-refractadmin-16ef4cf4"
namespace = "refract-dev"

# Get pod details
pod = api.read_namespaced_pod(name=pod_name, namespace=namespace)
print(pod.status)

event_list = []
progress = ""
field_selector = "involvedObject.name=" + pod_name
stream = watch.Watch().stream(api.list_namespaced_event,
                              namespace=namespace,
                              field_selector=field_selector,
                              timeout_seconds=1)


stage = {
        '1': {'status': 'waiting', 'logs': ''},
		'2': {'status': 'waiting', 'logs': ''},
		'3': {'status': 'waiting', 'logs': ''},
		'4': {'status': 'waiting', 'logs': ''}
        }

for event in stream:
    field_path = event["object"].involved_object.field_path

    if event["object"].event_time is None:
        progress = event["object"].type + " " + event["object"].message

    else:
        progress = date_time.strftime(event["object"].event_time, "%Y-%m-%d %H:%M:%S") \
                   + " " + event["object"].type + " " + event["object"].message

    if event not in event_list:
        event_list.append(progress)


    if field_path is not None:
        print(field_path + "  " + progress)
        if 'git-init' in field_path:
            stage['2']['logs'] = stage['2']['logs'] + progress + os.linesep
            if pod.status.init_container_statuses is not None:
                for container in pod.status.init_container_statuses:
                    if container.name == 'git-init':
                        if container.ready:
                            stage['2']['status'] = "success"

        if 'notebooks' in field_path:
            stage['3']['logs'] = stage['3']['logs'] + progress + os.linesep
            if pod.status.container_statuses is not None:

                for container in pod.status.container_statuses:
                    if container.name == 'notebooks':
                        if container.started:
                            stage['3']['status'] = "success"
                        else:
                            print(event["object"].reason)
                            if event["object"].reason == 'Failed':
                                nc_fail = 1
                                stage['3']['status'] = "failed"
                            else:
                                stage['3']['status'] = "loading"

        if 'knights-watch' in field_path:
            stage['4']['logs'] = stage['4']['logs'] + progress + os.linesep
            if pod.status.container_statuses is not None:
                for container in pod.status.container_statuses:
                    if container.name == 'knights-watch':
                        if container.started:
                            stage['4']['status'] = "success"
                        else:
                            print(event["object"].reason)
                            if event["object"].reason == 'Failed':
                                stage['4']['status'] = "failed"
                            else:
                                stage['4']['status'] = "loading"
    else:
        print("NONE - " + progress)


print(event_list)
print(progress)
print('----------------')
print(stage)