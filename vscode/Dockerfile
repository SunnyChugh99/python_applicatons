FROM codercom/code-server:latest
USER root
COPY snowflake.snowflake-vsc-1.1.1.vsix /home/coder/

RUN mkdir -p /notebooks/notebooks

RUN mkdir -p /config/data
RUN mkdir -p /config/extensions

RUN code-server --user-data-dir /config/data \
    --extensions-dir /config/extensions \
    --install-extension /home/coder/snowflake.snowflake-vsc-1.1.1.vsix

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    nginx \
    make \
    wget \
  &&  echo "**** cleanup ****"\
  &&  apt-get remove -y patch \
  &&  apt-get autoremove \
  &&  apt-get clean \
  &&  rm -rf  /tmp/*  /var/lib/apt/lists/*  /var/tmp/*

RUN rm /etc/nginx/nginx.conf
COPY nginx.conf /etc/nginx/nginx-base.conf

RUN chmod 777  -R /etc/nginx && \
    chmod 777 /etc /home /etc/profile.d


EXPOSE 8080
WORKDIR /home/mosaic-ai/
COPY entrypoint.sh entrypoint.sh

RUN echo "umask \$NB_UMASK" >> /.bashrc && echo "umask \$NB_UMASK" >> /etc/bash.bashrc && echo "umask \$NB_UMASK" >> /etc/bashrc &&  echo "umask \$NB_UMASK" >> /.shrc
ENTRYPOINT ["bash","entrypoint.sh"]