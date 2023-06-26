import os, json, requests
from datetime import datetime
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--type', type=str, required=True, help='Type of the event')
parser.add_argument('--reason', type=str, required=True, help='Reason for the event')

args = parser.parse_args()

namespace = open('/var/run/secrets/kubernetes.io/serviceaccount/namespace').read().strip()
pod_name = os.environ.get('HOSTNAME')
current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
event_name = f"my-event-{pod_name}-{current_time}"

message = f"{args.type} has {args.reason}"

event_payload = json.dumps({
    "metadata": {"name": event_name, "namespace": namespace},
    "involvedObject": {"kind": "Pod", "name": pod_name, "namespace": namespace},
    "reason": args.reason,
    "message": message,
    "type": args.type,
    "lastTimestamp": current_time
})

api_endpoint = f"https://{os.environ['KUBERNETES_SERVICE_HOST']}:{os.environ['KUBERNETES_SERVICE_PORT_HTTPS']}"
api_token = open('/var/run/secrets/kubernetes.io/serviceaccount/token').read().strip()

headers = {"Authorization": f"Bearer {api_token}", "Content-Type": "application/json"}
response = requests.post(f"{api_endpoint}/api/v1/namespaces/{namespace}/events", headers=headers, data=event_payload, verify=False)

if response.status_code != 201:
    print("Error creating event:", response.json()["message"])
    exit(1)
else:
    print("Event created:", response.json())
