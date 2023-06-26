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
            if event["object"].reason == 'Failed':
                stage['2'] = "failed"
            else:
                stage['2'] = "loading"



def handle_resource_allocation_event(stage, container_event):
    """Method to analyse progress and status of first stage-Allocating resource"""
    if container_event > 0:
        stage['1'] = "success"
    else:
        stage['1'] = "loading"

def handle_package_installation_event(event, pod, stage, field_path):
    if event["object"].type == 'Package-Installation':
        if event["object"].reason == 'Started':
            stage['3'] = "loading"
        if event["object"].reason == 'Completed':
            stage['3'] = "success"
            stage['4'] = "loading"

def handle_serving_event(event, pod, stage, field_path):
    if event["object"].type == 'Model':
        if event["object"].reason == 'DEPLOYED':
            stage['4'] = "success"
        if event["object"].reason == 'FAILED':
            stage['4'] = "fail"

def main():

    config.load_incluster_config()
    api = client.CoreV1Api()
    pod_name = "dp-0f10a14b-25c2-47be-8b47-def2501d5cf1-5fc8cd5754-d4v2g"
    namespace = open('/var/run/secrets/kubernetes.io/serviceaccount/namespace').read().strip()
    pod = api.read_namespaced_pod(name=pod_name, namespace=namespace)
    logging.info(pod.status)

    stage = {
     		'1': 'waiting',
     		'2': 'waiting',
     		'3': 'waiting',
            '4': 'waiting'
     }

    field_selector = "involvedObject.name=" + pod_name
    stream = watch.Watch().stream(api.list_namespaced_event,
                                  namespace=namespace,
                                  field_selector=field_selector,
                                  timeout_seconds=1)

    container_event = 0
    for event in stream:
        field_path = event["object"].involved_object.field_path
        #print(event["object"].type)
        #print(field_path)
        if field_path is not None:
            container_event += 1
            if container_event == 1:
                handle_resource_allocation_event(stage, container_event)
            handle_git_init_event(event, pod, stage, field_path)

        if container_event == 0:
            handle_resource_allocation_event(stage, container_event)
        handle_package_installation_event(event, pod, stage, field_path)
        handle_serving_event(event, pod, stage, field_path)
    print(stage)

if __name__ == '__main__':
    main()
