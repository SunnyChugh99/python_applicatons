@swag_from("../swag/get_feature_store.yaml")
def get_feature_store():
    """
    This method is used to get a feature store SDK stored in refract
    :param feature_store_name:
    :return: feature store SDK object
    """
    try:
        feature_store_name = request.args.get('feature_store_name')
        feature_yaml_path = get_feature_store_client(feature_store_name)

        print('content')
        print(feature_yaml_path)
        return send_file(f'{feature_yaml_path}feature_store.yaml', as_attachment=True)

    except Exception as ex:
        print('ex- view')
        print('printing ex')
        print(ex)
        print('p done')
        error_message = str(ex)  # Convert the exception to a string
        final_dict = {'error': error_message}
        print('printing error message')
        print(final_dict.get('error'))
        return jsonify(final_dict), 500  # Return the dictionary and set status_code to 500

def get_feature_store_client(feature_store_name):
    """
      This method is used to return feature store yaml file's path
      :param feature_store_name
      :return: feature_repo_temp_path
    """
    try:
        feature_store_info = g.db_session.query(FeatureStoreInfo).filter(FeatureStoreInfo.name == feature_store_name).first()
        if not feature_store_info:
            return jsonify({'error': 'No data found for the given repo_id'}), 404
        schema = FeatureStoreInfoSchema()
        response_data = schema.dump(feature_store_info)
        print('res data')
        print(response_data)
        print('checking proj access-1')
        print(g.userid)
        print(g.useremail)
        print(g.username)
        print(response_data.get('project_id'))
        print('api call')
        check_project_access(
            config.get("console-backend", "console_backend_url"),
            userid=g.userid,
            email=g.useremail,
            username=g.username,
            project_id=response_data.get('project_id'),
            access=True
        )
        print('checking proj access-2')
        feature_repo_temp_path = f"/tmp/{response_data.get('repo_id')}/feature_repo/"
        os.makedirs(feature_repo_temp_path, exist_ok=True)

        feature_store_yaml_creation(
            feature_repo_temp_path,
            response_data.get('name'),
            response_data.get('online_connection_details'),
            response_data.get('offline_connection_details')
        )
        return feature_repo_temp_path
    except Exception as ex:
        log.info(f'Error: {ex}')
        raise ex

import os
import requests
import tempfile

class FeastFeatureStore:
    def get_feature_store(self, feature_store_name):
        try:
            print('hi')
            from feast import FeatureStore
            headers = {
                "accept": "application/json",
                "X-Project-Id": os.getenv("PROJECT_ID"),
                'X-Auth-Userid': os.getenv("userId"),
                'X-Auth-Username': os.getenv("userId"),
                'X-Auth-Email': os.getenv("userId"),
            }

            base_url = "http://refract-common-service:5000/refract/common/api"
            url = f"{base_url}/v1/get_feature_store?feature_store_name={feature_store_name}"

            response = requests.get(url=url, headers=headers, verify=False)
            print('21')

            if response.status_code == 500:
                print('response')
                print(response)
                print('cont')
                print(response.content)
                return response.content

            print('t1')
            temp_dir = tempfile.mkdtemp()
            print('t2')

            yaml_path = os.path.join(temp_dir, "feature_store.yaml")
            print('yaml path')

            if response.status_code == 200:
                print('status code')
                with open(yaml_path, 'wb') as f:
                    f.write(response.content)
                store = FeatureStore(repo_path=temp_dir)
                return store
        except Exception as ex:
            print('ex')
            print(ex)
            return ex, 500
