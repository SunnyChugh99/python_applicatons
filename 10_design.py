from kubernetes import client, config, watch
from datetime import datetime as date_time
import logging
import os

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


def handle_event(event, pod, stage, field_path):
    """Method to analyze progress and status of different stages"""
    success_flags = [False] * 4
    if 'knights-watch' in field_path:
        container_statuses = pod.status.container_statuses
        container_name = 'knights-watch'
        stage_key = '4'
    elif 'git-init' in field_path:
        container_statuses = pod.status.init_container_statuses
        container_name = 'git-init'
        stage_key = '2'
    elif 'notebooks' in field_path:
        container_statuses = pod.status.container_statuses
        container_name = 'notebooks'
        stage_key = '3'
    else:
        return
    if container_statuses is not None:
        for container in container_statuses:
            if container.name == container_name:
                if container.ready:
                    stage[stage_key] = "success"
                    success_flags[int(stage_key)-1] = True

    if not success_flags[int(stage_key)-1]:
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
    pod_name = "jy-ffcf80ce-29a7-44ad-9678-a4e79cb77b49-refractadmin-16ef4cf4"
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
            handle_event(event, pod, stage, field_path)
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
