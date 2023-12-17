from kubernetes import client, config, watch
import logging
import os

class DeployStageStatus:
    """ client constant """
    SUCCESS = "success"
    LOADING = "loading"
    FAILED = "failed"
    WAITING = "waiting"

class EventType:
    """ client constant """
    PACKAGE_INSTALLATION = "Package-Installation"
    MODEL_SERVING = "Model-Serving"

class EventReason:
    """ client constant """
    NORMAL_EVENT_FAIL = "Failed"
    EVENT_COMPLETED = 'Completed'
    MODEL_SERVING_EVENT_FAIL = "FAILED"
    MODEL_SERVING_EVENT_COMPLETED = "DEPLOYED"



def stage_1(stage, container_event):
    stage['1'] = DeployStageStatus.SUCCESS if container_event > 0 else DeployStageStatus.LOADING

def stage_2(stage, field_path, pod, event_reason):
    if field_path is not None and pod.status.init_container_statuses is not None:
        containers_ready = any(container.ready for container in pod.status.init_container_statuses)
        stage['2'] = DeployStageStatus.SUCCESS if containers_ready else \
        DeployStageStatus.FAILED if 'git-init' in field_path and event_reason == EventReason.NORMAL_EVENT_FAIL else \
        DeployStageStatus.LOADING if 'git-init' in field_path else stage['2']
        stage['3'] = DeployStageStatus.LOADING if containers_ready else stage['3']

def stage_3(stage, field_path, pod, event_reason, event_type):
    if field_path and 'model' in field_path and event_reason == EventReason.NORMAL_EVENT_FAIL:
        stage['3'] = DeployStageStatus.FAILED

    if event_type == EventType.PACKAGE_INSTALLATION:
        stage['3'] = DeployStageStatus.SUCCESS if event_reason == EventReason.EVENT_COMPLETED else stage['3']
        stage['4'] = DeployStageStatus.LOADING if event_reason == EventReason.EVENT_COMPLETED else stage['4']

def stage_4(stage, field_path, pod, event_reason, event_type):
    if event_type == EventType.MODEL_SERVING:
        stage['4'] = DeployStageStatus.SUCCESS if event_reason == EventReason.MODEL_SERVING_EVENT_COMPLETED else \
            DeployStageStatus.FAILED if event_reason == EventReason.MODEL_SERVING_EVENT_FAIL else stage['4']

def finish_check(stage):
    num_waiting_loading = sum(1 for s in stage.values() if s in ('waiting', 'loading'))
    if num_waiting_loading == 0:
        print('inside')
        return True
    else:
        return False

def handle_event(event, pod, stage, field_path, container_event):
    global finished
    finished = False
    event_type = event["object"].type
    event_reason = event["object"].reason
    stage_1(stage, container_event)
    stage_2(stage, field_path, pod, event_reason)
    stage_3(stage, field_path, pod, event_reason, event_type)
    stage_4(stage, field_path, pod, event_reason, event_type)
    finished = finish_check(stage)

def get_pod_progress(pod_name):

    config.load_incluster_config()
    api = client.CoreV1Api()

    namespace = 'refract-dev'
    pod = api.read_namespaced_pod(name=pod_name, namespace=namespace)
    stage = {
     		'1': DeployStageStatus.WAITING,
     		'2': DeployStageStatus.WAITING,
     		'3': DeployStageStatus.WAITING,
            '4': DeployStageStatus.WAITING
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

    data = {'stage': stage, 'finished': finished}
    return data



if __name__ == '__main__':
    pod_name = "dp-a59dbf05-8958-4f3f-b106-f2cd2ba8cc31-867566bdcf-hf7gb"
    print(get_pod_progress(pod_name))
