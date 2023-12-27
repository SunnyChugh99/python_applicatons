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
                final_dict = response.content

                print("response json")
                final_dict = response.json()
                error_msg = final_dict.get('error')

                print('printing error msg')
                print(error_msg)
                return error_msg

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
