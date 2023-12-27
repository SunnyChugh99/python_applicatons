import os
import requests
import tempfile

class FeastFeatureStore:
    def get_feature_store(self, feature_store_name):
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

        print("store_obj - ", response)
        temp_dir = tempfile.mkdtemp()
        yaml_path = os.path.join(temp_dir, "feature_store.yaml")
        if response.status_code == 200:
            with open(yaml_path, 'wb') as f:
                f.write(response.content)
        store = FeatureStore(repo_path=temp_dir)
        return store

