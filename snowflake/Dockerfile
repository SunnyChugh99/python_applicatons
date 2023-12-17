#Using R-studio base image
FROM registry.lti-aiq.in:443/mosaic-ai-logistics/mosaic-notebooks-manager/rstudio:rs3.39-readonly_latest


#Installing odbc dependencies
RUN sudo apt-get update && sudo apt-get install -y libiodbc2-dev unixodbc
RUN R -e "install.packages(c('DBI', 'dplyr', 'dbplyr', 'odbc'), repos = 'http://cran.us.r-project.org', quiet = TRUE)"


WORKDIR /tmp

#downloading the snowflake odbc files
RUN wget https://sfc-repo.azure.snowflakecomputing.com/odbc/linux/2.25.0/snowflake-odbc-2.25.0.x86_64.deb


USER root
# installing the snowflake odbc files 
RUN dpkg -i snowflake-odbc-2.25.0.x86_64.deb



RUN rm /etc/odbc.ini
RUN rm /etc/odbcinst.ini


#First download and install the snowflake(using the above two command wget and dpkg) in local and while building r-studio image copy these files from local into the location where snowflake needs #at run time
COPY odbc.ini /etc/odbc.ini
COPY odbcinst.ini /etc/odbcinst.ini
COPY libSnowflake.so /usr/lib/x86_64-linux-gnu/odbc/libSnowflake.so
