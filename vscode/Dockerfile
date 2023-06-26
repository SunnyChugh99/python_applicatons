FROM registry.lti-aiq.in:443/mosaic-ai-logistics/mosaic-notebooks-manager/mosaic-docker-build/scala-vscode:2.0.3
USER root
COPY snowflake.snowflake-vsc-0.8.2.vsix /home/coder/

RUN code-server --user-data-dir /config/data \
    --extensions-dir /config/extensions \
    --install-extension /home/coder/snowflake.snowflake-vsc-0.8.2.vsix

USER mosaic-ai

