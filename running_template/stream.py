#/api/v1/namespaces/mosaic-services/events?fieldSelector=involvedObject.name%3Djy-a8a45aa4-6130-4e72-8f0d-3b616042b6d7-mosaic-b060d1d7-aaf2-46&timeoutSeconds=1&watch=True
#v1 = kubernetes.client.CoreV1Api() watch = kubernetes.watch.Watch() for e in watch.stream(v1.list_namespace, resource_version=1127):
# curl -k -v -H ‘X-Override-Host: refract.dev.fosfor.com’ -X GET /api/v1/namespaces/mosaic-services/events?fieldSelector=involvedObject.name%3Djy-a8a45aa4-6130-4e72-8f0d-3b616042b6d7-mosaic-b060d1d7-aaf2-46&timeoutSeconds=1&watch=True
# portal/plans
from kubernetes import client, config, watch
import kubernetes
print('1')
field_selector = "involvedObject.name=jy-2cb15189-5982-44dd-861b-dd01d08ec8bd-adminfosforcom-44539d"
from datetime import datetime as date_time
api = kubernetes.client.CoreV1Api()
print('2')
stream = kubernetes.watch.Watch().stream(api.list_namespaced_event,
                               namespace="test-ai-logistics",
                               field_selector=field_selector,
                               timeout_seconds=10)
progress = ""
print('3')
print(stream)
print('4')
#stream = curl -k -v -H ‘X-Override-Host: refract.dev.fosfor.com’ -X GET /api/v1/namespaces/mosaic-services/events?fieldSelector=involvedObject.name%3Djy-a8a45aa4-6130-4e72-8f0d-3b616042b6d7-mosaic-b060d1d7-aaf2-46&timeoutSeconds=1&watch=True

for event in stream:
    print('5')
    if event["object"].event_time is None:
        progress = event["object"].type + " " + event["object"].message
    else:
        progress = date_time.strftime(event["object"].event_time, "%Y-%m-%d %H:%M:%S") \
                   + " " + event["object"].type + " " + event["object"].message

print(progress)