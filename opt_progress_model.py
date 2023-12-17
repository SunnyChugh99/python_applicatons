from kubernetes import client, config, watch
import logging
import os

def handle_event(event, pod, stage, field_path, container_event):
    if event["object"].type == 'Package-Installation':
        if event["object"].reason == 'Started':
            stage['3'] = "loading"
        if event["object"].reason == 'Completed':
            stage['3'] = "success"
            stage['4'] = "loading"
    elif event["object"].type == 'Model':
        if event["object"].reason == 'DEPLOYED':
            stage['4'] = "success"
        if event["object"].reason == 'FAILED':
            stage['4'] = "fail"

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

    if container_event > 0:
        stage['1'] = "success"
    else:
        stage['1'] = "loading"


def main():

    config.load_incluster_config()
    api = client.CoreV1Api()
    pod_name = "dp-70f54412-3f4f-48c7-b1e8-4183b7612caa-5bff5755c-szv6r"
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
        if field_path is not None:
            container_event += 1
        handle_event(event, pod, stage, field_path, container_event)
    print(stage)

if __name__ == '__main__':
    main()
