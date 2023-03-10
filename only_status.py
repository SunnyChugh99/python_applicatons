from kubernetes import client, config, watch
from datetime import datetime as date_time
import logging
import os

def handle_git_init_event(event, pod, stage, field_path):
    success_flag = False
    if pod.status.init_container_statuses is not None:
        for container in pod.status.init_container_statuses:
            if container.ready:
                stage['2'] = "success"
                success_flag = True
    if not success_flag:
        if 'git-init' in field_path:
            progress = get_event_progress(event)
            if event["object"].reason == 'Failed':
                stage['2'] = "failed"
            else:
                stage['2'] = "loading"


def handle_notebooks_event(event, pod, stage, field_path):
    success_flag = False
    if pod.status.container_statuses is not None:
        for container in pod.status.container_statuses:
            if container.name == 'notebooks':
                if container.ready:
                    stage['3'] = "success"
                    success_flag = True
    if not success_flag:
        if 'notebooks' in field_path:
            if event["object"].reason == 'Failed':
                stage['3'] = "failed"
            else:
                stage['3'] = "loading"


def handle_knights_watch_event(event, pod, stage, field_path):
    success_flag = False
    if pod.status.container_statuses is not None:
        for container in pod.status.container_statuses:
            if container.name == 'knights-watch':
                if container.ready:
                    stage['4'] = "success"
                    success_flag = True
    if not success_flag:
        if 'knights-watch' in field_path:
            if event["object"].reason == 'Failed':
                stage['4'] = "failed"
            else:
                stage['4'] = "loading"


def handle_null_event(event, stage, fp_c):
    if fp_c > 0:
        stage['1'] = "success"
    else:
        stage['1'] = "loading"



def get_event_progress(event):
    if event["object"].event_time is None:
        return event["object"].type + " " + event["object"].message
    else:
        return date_time.strftime(event["object"].event_time, "%Y-%m-%d %H:%M:%S") \
            + " " + event["object"].type + " " + event["object"].message


def handle_notebooks_knights_event(event, pod, stage, field_path, container_name, stage_key):
    """Method to analyse progress and status of third and fourth stages"""
    success_flag = [False, False]
    if pod.status.container_statuses is not None:
        for container in pod.status.container_statuses:
            if container.name == container_name:
                if container.ready:
                    stage[stage_key] = "success"
                    success_flag[int(stage_key)-3] = True
    if not success_flag[int(stage_key)-3]:
        if container_name in field_path:
            if event["object"].reason == 'Failed':
                stage[stage_key] = "failed"
            else:
                stage[stage_key] = "loading"

def main():
    # Load Kubernetes configuration
    config.load_incluster_config()
    import argparse

    # Create Kubernetes client
    api = client.CoreV1Api()
    # parser = argparse.ArgumentParser()
    # parser.add_argument("pod_name", help="Name of the pod to retrieve")
    #
    # args = parser.parse_args()
    # # Define pod name and namespace
    pod_name = "jy-991fe736-6b43-40c7-b193-f8a84f64271c-refractadmin-af74ae22"
    namespace = "refract-dev"

    # Get pod details
    pod = api.read_namespaced_pod(name=pod_name, namespace=namespace)
    logging.info(pod.status)

    # Set up logging
    logging.basicConfig(filename='events.log', level=logging.INFO, format='%(asctime)s [%(levelname)s]: %(message)s')

    # Define stage details
    stage = {
     		'1': 'waiting',
     		'2': 'waiting',
     		'3': 'waiting',
            '4': 'waiting'
     }

    # Watch for events
    event_list = []
    field_selector = "involvedObject.name=" + pod_name
    stream = watch.Watch().stream(api.list_namespaced_event, namespace=namespace, field_selector=field_selector,
                                  timeout_seconds=10)

    fp_c = 0
    for event in stream:
        #get_event_progress(event)
        field_path = event["object"].involved_object.field_path
        print('aa')
        print(field_path)
        if field_path is not None:
            fp_c += 1
            if fp_c == 1:
                handle_null_event(event, stage, fp_c)
            handle_git_init_event(event, pod, stage, field_path)
            handle_notebooks_knights_event(event, pod, stage, field_path, "notebooks", '3')
            handle_notebooks_knights_event(event, pod, stage, field_path, "knights-watch", '4')
        if fp_c == 0:
            handle_null_event(event, stage, fp_c)


    print("--------------------------")
    print(pod.status.container_statuses)
    print("--------------------------")
    print(stage)
    print('--------------------------------------------------------')
    print('--------------------------------------------------------')
    print(pod.status.container_statuses)

    #stage = {'1': 'success', '2': 'success', '3': 'success', '4': 'success'}
    success_count = list(stage.values()).count('success')
    progress_perc = 25 * success_count
    print(progress_perc)

if __name__ == '__main__':
    main()
