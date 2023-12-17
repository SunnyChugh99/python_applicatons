FROM registry.access.redhat.com/ubi8/openjdk-11
USER root

#RUN microdnf remove -y gzip
RUN rm -rf /lib/python3.6/site-packages/setuptools \
&& rm -rf /lib/python3.6/site-packages/setuptools-39.2.0.dist-info

#RUN rm -fR /opt/jboss/keycloak/*
RUN mkdir -p /app

COPY keycloak-20.0.1 /app

RUN chown -R jboss /app
RUN chmod -R a+x /app
USER jboss

ENTRYPOINT ["/app/start.sh"]
