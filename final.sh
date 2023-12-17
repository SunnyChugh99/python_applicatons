#!/bin/bash

# Set the namespace and pod name
#namespace="refract-dev"
#namespace=$NAMESPACE
namespace=$(cat /var/run/secrets/kubernetes.io/serviceaccount/namespace)

pod_name=$HOSTNAME

# Set the event name and timestamps
current_time=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
event_name="my-event-${pod_name}-${current_time}"
last_timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Define the event payload as a JSON string
event_payload="{\"metadata\":{\"name\":\"${event_name}\",\"namespace\":\"${namespace}\"},\"involvedObject\":{\"kind\":\"Pod\",\"name\":\"${pod_name}\",\"namespace\":\"${namespace}\"},\"reason\":\"sunnyTest\",\"message\":\"This is a bash event\",\"type\":\"Bashinstallation\",\"lastTimestamp\":\"${last_timestamp}\"}"

# Define the Kubernetes API endpoint and token
#api_endpoint="https://kubernetes.default.svc"
api_endpoint="https://${KUBERNETES_SERVICE_HOST}:${KUBERNETES_SERVICE_PORT_HTTPS}"

api_token=$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)

# Create the event using the Kubernetes API
response=$(curl -s -k -H "Authorization: Bearer ${api_token}" -H "Content-Type: application/json" -X POST --data "${event_payload}" "${api_endpoint}/api/v1/namespaces/${namespace}/events")

# Check the response for errors
if [[ $(echo "${response}" | grep -o "\"kind\":\"[^\"]*" | cut -d "\"" -f 4) == "Status" ]]; then
  echo "Error creating event:"
  echo "${response}" | jq -r '.message'
  exit 1
else
  echo "Event created"
  echo "${response}"
fi
