event_name="my-event-${HOSTNAME}-$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
event_payload="{\"metadata\":{\"name\":\"${event_name}\",\"namespace\":\"$(cat /var/run/secrets/kubernetes.io/serviceaccount/namespace)\"},\"involvedObject\":{\"kind\":\"Pod\",\"name\":\"${HOSTNAME}\",\"namespace\":\"$(cat /var/run/secrets/kubernetes.io/serviceaccount/namespace)\"},\"reason\":\"Completed\",\"message\":\"Package installation has Started\",\"type\":\"packageinstallation\",\"lastTimestamp\":\"$(date -u +"%Y-%m-%dT%H:%M:%SZ")\"}"

api_endpoint="https://${KUBERNETES_SERVICE_HOST}:${KUBERNETES_SERVICE_PORT_HTTPS}"
api_token=$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)
response=$(curl -s -k -H "Authorization: Bearer ${api_token}" -H "Content-Type: application/json" -X POST --data "${event_payload}" "${api_endpoint}/api/v1/namespaces/$(cat /var/run/secrets/kubernetes.io/serviceaccount/namespace)/events")

# Check the response for errors
if [[ $(echo "${response}" | grep -o "\"kind\":\"[^\"]*" | cut -d "\"" -f 4) == "Status" ]]; then
  echo "Error creating event:"
  echo "${response}" | grep -Po '"message":.*?[^\\]",' | sed 's/"message"://;s/^"\|",$//g'
  exit 1
else
  echo "Event created"
  echo "${response}"
fi

