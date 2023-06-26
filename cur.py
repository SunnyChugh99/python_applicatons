from kubernetes import client, config, watch


def stream(testing=None):
    api_client = client.ApiClient()
    api_instance = client.CoreV1Api(api_client)
    pod_name = "jy-869f690f-a4d7-435a-9ef8-137b376dfcc6-refractadmin-af74ae22"
    namespace = "refract-dev"
    container_name = "notebooks"
    follow = False
    previous = False
    _params = dict(name=pod_name,
                   namespace=namespace,
                   container=container_name,
                   tail_lines=10,
                   follow=follow,
                   previous=previous)

    log_stream = watch.Watch().stream(api_instance.read_namespaced_pod_log,
                                            **_params)
    while True:
        for chunk_ in log_stream:
            try:
                yield f"{chunk_}\n"
            # pylint: disable=broad-except
            except Exception as ex:
                print(ex)

        if testing:
            break

log_stream = stream()

for log in log_stream:
    print(log)
