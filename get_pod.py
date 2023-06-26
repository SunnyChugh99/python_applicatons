from kubernetes import client, config


def get_pods(deployment_name, response_type='POD_NAMES'):
    """
    Args:
        deployment_name: Name of the deployment
        response_type: response type such as 'POD NAMES' and 'POD_OBJECT'
    Returns:
        response_type 'POD_NAMES' will return the list of pod names and 'POD_OBJECT' will
        return the list of pod objects.
    """
    config.load_incluster_config()

    api = client.CoreV1Api()

    namespace = 'refract-dev'
    pods = []
    try:
        app_api = client.AppsV1Api()
        response = app_api.read_namespaced_deployment(deployment_name, namespace)
        label_value = response.to_dict().get("metadata").get("labels").get("app")
        api_response = api.list_namespaced_pod(namespace,
                                               label_selector='app={}'.format(label_value))

        api_response = api.list_namespaced_pod(namespace,
                                               label_selector='app={}'.format(label_value))
        pods = []
        for item in sorted(api_response.items, key=lambda x: x.metadata.creation_timestamp):
            if item.metadata.name.startswith(deployment_name):
                pod_name = item.metadata.name
                pod_timestamp = item.metadata.creation_timestamp.strftime("%Y-%m-%d %H:%M:%S")
                pods.append(pod_name if response_type == "POD_NAMES" else item)


    # pylint: disable=broad-except, logging-not-lazy
    except Exception as ex:
        # pylint: disable=logging-not-lazy
        # log.exception("Exception when calling CoreV1Api->list_namespaced_pod: %s\n" % ex)
        # raise exception
        print(ex)

    return pods



data = get_pods('mosaic-ai-backend')
print(data)
