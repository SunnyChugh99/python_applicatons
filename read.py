[200~Dependency Installation started


mkdir: cannot create directory ‘/mosaic_data/pre_build’: Permission denied


Folder created


File created


Dependency Installation completed


/tmp/tmp6jau2wy2


[uWSGI] getting INI configuration from /mosaic-ai-serving/configs/uwsgi-server.ini


*** Starting uWSGI 2.0.19.1 (64bit) on [Fri Mar 10 09:55:54 2023] ***


compiled with version: 9.3.0 on 02 March 2021 12:41:15


os: Linux-5.4.219-126.411.amzn2.x86_64 #1 SMP Wed Nov 2 17:44:17 UTC 2022


nodename: dp-2539ffd2-0bed-4de4-bf26-ec7c2654155b-559965855d-7ksw6


machine: x86_64


clock source: unix


pcre jit disabled


detected number of CPU cores: 8


current working directory: /home/mosaic-ai


detected binary path: /opt/conda/bin/uwsgi


*** WARNING: you are running uWSGI without its master process manager ***


your memory page size is 4096 bytes


detected max file descriptor number: 1048576


lock engine: pthread robust mutexes


thunder lock: disabled (you can enable it with --thunder-lock)


uwsgi socket 0 bound to TCP address 0.0.0.0:5001 fd 3


Python version: 3.7.10 | packaged by conda-forge | (default, Feb 19 2021, 16:07:37)  [GCC 9.3.0]


Python main interpreter initialized at 0x55d72e4632a0


python threads support enabled


your server socket listen backlog is limited to 100 connections


your mercy for graceful operations on workers is 60 seconds


mapped 834447 bytes (814 KB) for 9 cores


*** Operational MODE: preforking+threaded ***


Model loaded for deployment


INFO:mosaic_serving:Model loaded for deployment


Score function loaded for deployment


INFO:mosaic_serving:Score function loaded for deployment


DEBUG:urllib3.connectionpool:Starting new HTTP connection (1): mosaic-ai-backend:5000


DEBUG:urllib3.connectionpool:http://mosaic-ai-backend:5000 "GET /registry/api/v1/ml-model/68c5f661-1cd8-4b0d-8c39-b8ebcf3a0843 HTTP/1.1" 200 6604


DEBUG:urllib3.connectionpool:Starting new HTTP connection (1): mosaic-ai-backend:5000


DEBUG:urllib3.connectionpool:http://mosaic-ai-backend:5000 "GET /registry/api/v1/ml-model/68c5f661-1cd8-4b0d-8c39-b8ebcf3a0843/version/6a82c4f3-690b-4929-ba74-b2ae5b0f1305 HTTP/1.1" 200 3801


DEBUG:urllib3.connectionpool:Starting new HTTP connection (1): mosaic-ai-backend:5000


DEBUG:urllib3.connectionpool:http://mosaic-ai-backend:5000 "GET /registry/api/v1/ml-model/deploy/2539ffd2-0bed-4de4-bf26-ec7c2654155b HTTP/1.1" 403 0


DEBUG:urllib3.connectionpool:Starting new HTTP connection (1): mosaic-ai-backend:5000


DEBUG:urllib3.connectionpool:http://mosaic-ai-backend:5000 "POST /registry/api/v1/ml-model/deploy/2539ffd2-0bed-4de4-bf26-ec7c2654155b HTTP/1.1" 200 0


Current Deployment Status DEPLOYED


DEBUG:mosaic_serving:Current Deployment Status DEPLOYED


Current Deployment Status DEPLOYED


INFO:mosaic_serving:Current Deployment Status DEPLOYED


WSGI app 0 (mountpoint='') ready in 2 seconds on interpreter 0x55d72e4632a0 pid: 47 (default app)


spawned uWSGI worker 1 (pid: 47, cores: 3)


spawned uWSGI worker 2 (pid: 64, cores: 3)


spawned uWSGI worker 3 (pid: 67, cores: 3)[201~
