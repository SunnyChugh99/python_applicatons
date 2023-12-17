#!/bin/bash

# Set the namespace and pod name
namespace="refract-dev"
pod_name="dp-9dacf3d8-7963-467b-8929-803f47d64242-849969688f-8nkk5"

# Set the event name and timestamp
timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
event_name="my-event-${pod_name}-${timestamp}"

# Define the event payload as a JSON string
event_payload="{\"metadata\":{\"name\":\"${event_name}\",\"namespace\":\"${namespace}\"},\"involvedObject\":{\"kind\":\"Pod\",\"name\":\"${pod_name}\",\"namespace\":\"${namespace}\"},\"reason\":\"sunnyTest\",\"message\":\"This is a bash event\",\"type\":\"Bashinstallation\"}"

# Create the event using kubectl
response=$(curl -s -k -H "Content-Type: application/json" -X POST --data "${event_payload}" "https://kubernetes.default.svc/api/v1/namespaces/${namespace}/events")

# Check the response for errors
if [[ $(echo "${response}" | grep -o "\"kind\":\"[^\"]*" | cut -d "\"" -f 4) == "Status" ]]; then
  echo "Error creating event:"
  echo "${response}" | jq -r '.message'
  exit 1
else
  echo "Event created"
  echo "${response}"
fi
