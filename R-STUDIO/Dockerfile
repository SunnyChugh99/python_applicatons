FROM registry.lti-aiq.in:443/sunny.chugh/mosaic-notebooks-manager/rstudio:FIX2
USER root
RUN conda install -c conda-forge r-xlsx --yes
RUN R -e "dyn.load('/opt/miniconda/jre/lib/amd64/server/libjvm.so')"
USER rstudio
