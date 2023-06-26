FROM registry.lti-aiq.in:443/mosaic-ai-logistics/mosaic-notebooks-manager/mosaic-docker-build/scala-vscode:2.0.3
USER root
COPY snowflake.snowflake-vsc-1.1.1.vsix /home/coder/

RUN code-server --user-data-dir /config/data \
    --extensions-dir /config/extensions \
    --install-extension /home/coder/snowflake-extension.vsix

USER mosaic-ai

