from flask import g, jsonify, Response
import requests

def check_project_access_for_feature_store(console_url, project_id):
    """
     function for checking project access containing feature store

      Args:
          :param console_url:
          :param project_id:

      """

    project_access_url = f"{console_url}/secured/api/project/v1/access"
    headers = {
        "X-Auth-Username": 'refract.admin',
        "X-Auth-Userid": 'refract.admin',
        "X-Auth-Email": '',
        "X-Project-Id": project_id
    }
    response = requests.get(project_access_url, headers=headers)
    if response.status_code == 404 or response.status_code == 401:
        # raise exception
        return Response("Access denied for project containing given feature store", status=403)
    if response.status_code == 500:
        if "not authorised" in response.json()["message"]:
            raise ValueError("Access denied for project containing given feature store.")
        if "not found" in response.json()["message"]:
            raise ValueError("Project containing given feature store has been delete, please redeploy feature store")
    if response.status_code == 200 and response.json()["accessType"] not in ["OWNER", "CONTRIBUTOR", "VALIDATOR"]:
        raise ValueError("Access denied for project containing given feature store")


check_project_access_for_feature_store(
       "http://mosaic-console-backend/mosaic-console-backend",
        project_id="e80e8832-48ba-4607-b6c6-fc2c6727c5c8"
        )