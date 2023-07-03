FROM codercom/code-server:latest

USER root
RUN apt-get update && apt-get install -y python3-pip
ENV PATH=/usr/bin:$PATH
# pip package installation path [read only root file system]
RUN pip config  set global.target /tmp/pip_packages
ENV PYTHONPATH "${PYTHONPATH}:/tmp/pip_packages"

COPY snowflake.snowflake-vsc-1.1.1.vsix /home/coder/
COPY Phu1237.vs-browser-2.0.10.vsix /home/coder/
COPY ms-toolsai.jupyter-2023.6.1001821100.vsix /home/coder/
RUN mkdir -p /notebooks/notebooks

RUN mkdir -p /config/data
RUN mkdir -p /config/extensions

RUN code-server --user-data-dir /config/data \
     --extensions-dir /config/extensions \
     --install-extension /home/coder/snowflake.snowflake-vsc-1.1.1.vsix

RUN code-server --user-data-dir /config/data \
     --extensions-dir /config/extensions \
     --install-extension /home/coder/Phu1237.vs-browser-2.0.10.vsix

RUN code-server --user-data-dir /config/data \
     --extensions-dir /config/extensions \
     --install-extension /home/coder/ms-toolsai.jupyter-2023.6.1001821100.vsix

RUN code-server --install-extension /home/coder/ms-toolsai.jupyter-2023.6.1001821100.vsix --force


RUN pip install streamlit

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    nginx \
    make \
    wget \
  &&  echo "**** cleanup ****"\
  &&  apt-get remove -y patch \
  &&  apt-get autoremove -y \
  &&  apt-get clean -y \
  &&  rm -rf  /tmp/*  /var/lib/apt/lists/*  /var/tmp/*

RUN rm /etc/nginx/nginx.conf
COPY nginx.conf /etc/nginx/nginx-base.conf

RUN chmod 777  -R /etc/nginx && \
    chmod 777 /etc /home /etc/profile.d


# set permissions for mosaic-ai user
RUN useradd -ms /bin/bash -G sudo mosaic-ai
RUN echo "mosaic-ai ALL=(ALL) ALL" >> /etc/sudoers
RUN echo "%mosaic-ai ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

RUN mkdir -p /notebooks/notebooks && \
 mkdir -p /config/data && \
 mkdir -p /config/extensions && \
 chown -R "mosaic-ai":"mosaic-ai" /config && \
 chown -R "mosaic-ai":"mosaic-ai" /notebooks && \
 chown -R "mosaic-ai":"mosaic-ai" /etc/nginx/

RUN chmod 777  -R /etc/nginx /home/mosaic-ai && \
    chmod 777 /etc /home /etc/profile.d

EXPOSE 8080
WORKDIR /home/mosaic-ai/
COPY entrypoint.sh entrypoint.sh
COPY create_user.sh /create_user.sh
RUN chown -R "mosaic-ai":"mosaic-ai" entrypoint.sh
RUN chown -R "mosaic-ai":"mosaic-ai" /create_user.sh && chmod 777 /create_user.sh

RUN echo "umask \$NB_UMASK" >> /.bashrc && echo "umask \$NB_UMASK" >> /etc/bash.bashrc && echo "umask \$NB_UMASK" >> /etc/bashrc &&  echo "umask \$NB_UMASK" >> /.shrc
USER mosaic-ai
RUN python3 -m pip install notebook
RUN python3 -m pip install ipykernel

RUN python3 -m ipykernel install --user
ENTRYPOINT ["bash","entrypoint.sh"]