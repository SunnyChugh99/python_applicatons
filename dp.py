import os
import json
import requests
from datetime import datetime

# Set the namespace and pod name
namespace = open('/var/run/secrets/kubernetes.io/serviceaccount/namespace').read().strip()
pod_name = os.environ.get('HOSTNAME')

# Set the event name and timestamps
current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
event_name = f"my-event-{pod_name}-{current_time}"
last_timestamp = current_time

# Define the event payload as a JSON string
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
    "reason": "sunnyTest",
    "message": "This is a Python event",
    "type": "PythonInstallation",
    "lastTimestamp": last_timestamp
}
event_payload = json.dumps(event_payload)

# Define the Kubernetes API endpoint and token
api_endpoint = "https://kubernetes.default.svc"
api_token = open('/var/run/secrets/kubernetes.io/serviceaccount/token').read().strip()

# Create the event using the Kubernetes API
headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json"
}
response = requests.post(f"{api_endpoint}/api/v1/namespaces/{namespace}/events", headers=headers, data=event_payload, verify=False)

# Check the response for errors
if response.status_code != 201:
    print("Error creating event:")
    print(response.json()["message"])
    exit(1)
else:
    print("Event created")
    print(response.json())
