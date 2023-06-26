#!/bin/bash
set -x # Activate debugging to show execution details: all commands will be printed before execution

echo "Entrypoint..."


# replace BASE_URL with environment variable set
cp /etc/nginx/nginx-base.conf /tmp/nginx-base.conf
sed 's;$BASE_URL;'"$BASE_URL"';' /tmp/nginx-base.conf >> /tmp/nginx.conf


nginx -g "daemon off;" -c /tmp/nginx.conf &
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start Nginx: $status"
  exit $status
fi

mkdir -p /tmp/data/User
echo '{ "files.exclude": { "**/.classpath": true, "**/.project": true, "**/.settings": true,"**/.factorypath": true}, "terminal.integrated.defaultProfile.linux": "bash"}' > /tmp/data/User/settings.json
mkdir -p /tmp/extensions
cp -r /config/extensions/* /tmp/extensions/


/usr/bin/code-server \
			--bind-addr 0.0.0.0:8443 \
			--verbose \
			--config /tmp/code-server/config.yaml \
			--user-data-dir /tmp/data \
			--extensions-dir /tmp/extensions \
			--disable-telemetry \
			--auth "none" \
			/notebooks/notebooks &
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start Code-Server: $status"
  exit $status
fi



while sleep 60; do
  ps aux |grep nginx |grep -q -v grep
  PROCESS_1_STATUS=$?
  ps aux |grep code-server |grep -q -v grep
  PROCESS_2_STATUS=$?


  if [ $PROCESS_1_STATUS -ne 0 -o $PROCESS_2_STATUS -ne 0 ]; then
    echo "One of the processes has already exited."
    exit 1
  fi
done