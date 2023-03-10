from kubernetes import client, config, watch
from datetime import datetime as date_time
import logging
import os
# Load Kubernetes configuration
# config.load_incluster_config()
#
# # Create Kubernetes client
# api = client.CoreV1Api()
#
# # Define pod name and namespace
# #pod_name = "jy-844ad592-5758-4e41-911d-613801ed9d4b-refractadmin-16ef4cf4"
# #pod_name = "jy-12a90fb4-2a25-41a3-9d24-5b4956b59530-refractadmin"
# namespace = "refract-dev"
#
# # Get pod details
# pod = api.read_namespaced_pod(name=pod_name, namespace=namespace)
# logging.info(pod.status)
#
# # Set up logging
# logging.basicConfig(filename='events.log', level=logging.INFO,
#                     format='%(asctime)s [%(levelname)s]: %(message)s')
#
# # Define stage details
# stage = {
#     '1': {'status': 'waiting', 'logs': ''},
#     '2': {'status': 'waiting', 'logs': ''},
#     '3': {'status': 'waiting', 'logs': ''},
#     '4': {'status': 'waiting', 'logs': ''}
# }
# stage = {
# 		'1' : 'waiting'
# 		'2' : 'waiting',
# 		'3' : 'waiting',
#         '4' : 'waiting',
# }

# Define helper functions
# Define helper functions
def handle_git_init_event(event, pod, stage, field_path):
    success_flag = False
    progress = ""
    if pod.status.init_container_statuses is not None:
        for container in pod.status.init_container_statuses:
            if container.ready:
                stage['2']['status'] = "success"
                success_flag = True
    if not success_flag:
        if 'git-init' in field_path:
            progress = get_event_progress(event)
            stage['2']['logs'] += progress + os.linesep
            if event["object"].reason == 'Failed':
                stage['2']['status'] = "failed"
            else:
                stage['2']['status'] = "loading"
    print(f'git-init event: {progress}')
    print("------")
    print(event["object"].reason)
    print("------")


def handle_notebooks_event(event, pod, stage, field_path):
    progress = ""
    if 'notebooks' in field_path:
        progress = get_event_progress(event)
        stage['3']['logs'] += progress + os.linesep
    if pod.status.container_statuses is not None:
        for container in pod.status.container_statuses:
            if container.name == 'notebooks':
                print(container.ready)
                if container.ready:
                    stage['3']['status'] = "success"
                elif 'notebooks' in field_path:
                    logging.info(f'notebooks event reason: {event["object"].reason}')
                    if event["object"].reason == 'Failed':
                        stage['3']['status'] = "failed"
                    else:
                        stage['3']['status'] = "loading"
    print(f'notebooks event: {progress}')


def handle_knights_watch_event(event, pod, stage, field_path):
    progress = ""
    if 'knights-watch' in field_path:
        progress = get_event_progress(event)
        stage['4']['logs'] += progress + os.linesep
    print('inside KW')
    if pod.status.container_statuses is not None:
        for container in pod.status.container_statuses:

            if container.name == 'knights-watch':
                print(container.ready)
                if container.ready:
                    stage['4']['status'] = "success"
                else:
                    logging.info(f'knights-watch event reason: {event["object"].reason}')
                    if event["object"].reason == 'Failed':
                        stage['4']['status'] = "failed"
                    else:
                        stage['4']['status'] = "loading"
    print(f'knights-watch event: {progress}')


def handle_null_event(event, stage, fp_c):
    progress = get_event_progress(event)
    if fp_c > 0:
        stage['1']['status'] = "success"
    else:
        stage['1']['status'] = "loading"
        stage['1']['logs'] += progress + os.linesep


def get_event_progress(event):
    if event["object"].event_time is None:
        return event["object"].type + " " + event["object"].message
    else:
        return date_time.strftime(event["object"].event_time, "%Y-%m-%d %H:%M:%S") \
            + " " + event["object"].type + " " + event["object"].message



def main():
    # Load Kubernetes configuration
    config.load_incluster_config()
    import argparse

    # Create Kubernetes client
    api = client.CoreV1Api()
    parser = argparse.ArgumentParser()
    parser.add_argument("pod_name", help="Name of the pod to retrieve")

    args = parser.parse_args()
    # Define pod name and namespace
    pod_name = args.pod_name
    namespace = "refract-dev"

    # Get pod details
    pod = api.read_namespaced_pod(name=pod_name, namespace=namespace)
    logging.info(pod.status)

    # Set up logging
    logging.basicConfig(filename='events.log', level=logging.INFO, format='%(asctime)s [%(levelname)s]: %(message)s')

    # Define stage details
    stage = {
        '1': {'status': 'waiting', 'logs': ''},
        '2': {'status': 'waiting', 'logs': ''},
        '3': {'status': 'waiting', 'logs': ''},
        '4': {'status': 'waiting', 'logs': ''}
    }




    # Watch for events
    event_list = []
    field_selector = "involvedObject.name=" + pod_name
    stream = watch.Watch().stream(api.list_namespaced_event, namespace=namespace, field_selector=field_selector, timeout_seconds=1)

    fp_c = 0
    for event in stream:
        #get_event_progress(event)
        field_path = event["object"].involved_object.field_path

        print(field_path)
        if field_path is not None:
            fp_c += 1
            if fp_c == 1:
                handle_null_event(event, stage, fp_c)
#            if 'git-init' in field_path:
            handle_git_init_event(event, pod, stage, field_path)
#            if 'notebooks' in field_path:
            handle_notebooks_event(event, pod, stage, field_path)
#            if 'knights-watch' in field_path:
            handle_knights_watch_event(event, pod, stage, field_path)
        if fp_c == 0:
            handle_null_event(event, stage, fp_c)

    print(stage)
    print('--------------------------------------------------------')
    print(pod.spec.node_name)
    print('--------------------------------------------------------')
    print(pod.status.container_statuses)

if __name__ == '__main__':
    main()
