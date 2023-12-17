from kubernetes import client, config, watch
from flask import request, Response, jsonify, g, stream_with_context, current_app

def get_pod_progress(pod_name, port_no, ingress_url, kernel_type=None):
    """Method to return pod ip progress"""
    try:
        print('111222')
        data = []
        api = client.CoreV1Api()
        resp = api.read_namespaced_pod(name=pod_name, namespace="refract-dev")

        print('1112222234443')
        return data
    except Exception as e:
        raise e



def progress(pod_name):
    """Stream method"""
    port_no = "8889"
    ingress_url = "/templates/e47f564a24eebbd048947a8ec367a682/1ff98a53-ff2d-4a8d-84fe-dc1b8feb9e16/Python-3.7-16ef4cf4-6ebb-4598-9daa-181e578de4d5/"
    kernel_type = "python"
    print('111')
    def event_stream():
        """event stream method"""

        try:
            print('1')
            api = client.CoreV1Api()
            resp = api.read_namespaced_pod(name=pod_name, namespace="refract-dev")
            print('3')
        except Exception as e:
            print('2')
            return_message = {"message": str(e), "progress": 100}
            return_string = "data: {}".format(return_message)
            return return_string

    print('1234')
    return event_stream()

print(progress("jy-1ff98a53-ff2d-4a8d-84fe-dc1b8feb9e16-refractadmin-16ef4cf4"))