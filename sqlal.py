#GET-	https://dev.refract-fosfor.com/vcs/api/v1/download/repo/af74ae22-cc77-4a24-96ee-1a72d295b4db/file/test13/branch/dev/isfolder/true
# /v1/download/repo/<string:repo>/file/<path:file_path>/branch/<path:branch>/isfolder/<path:isfolder>"
repo = "af74ae22-cc77-4a24-96ee-1a72d295b4db"
file_path = "test13"
isfolder = "true"
branch = "dev"
repo_url = "https://git.lti-aiq.in/mosaic-ai-qa-user/b0c37851-7c22-4737-8d9a-c49899de2c36.git"
from gitlab import Gitlab
import shutil

client = Gitlab(repo_url, private_token="N8j4YdMncsH8jbVh")
from urllib.parse import urlparse
repo_name = urlparse(repo_url).path.replace(".git", "")[1:]
from pathlib import Path
import os
from zipfile import ZipFile

get_file_list = [{'id': 'f3287f557cc556ffaa8322eeb2af9c7a3cf56320', 'name': 'f2', 'type': 'tree', 'path': 'test14/f2', 'mode': '040000'}, {'id': '38363baaf368da00caa349345186800059f12334', 'name': 'inside_14', 'type': 'tree', 'path': 'test14/inside_14', 'mode': '040000'}, {'id': '205190ef0a5bd9a6ee2fa7045406b44bce1f7dde', 'name': 'normal', 'type': 'tree', 'path': 'test14/normal', 'mode': '040000'}, {'id': '9f38eff59aa981d6b596e5fd3e54aceb84dc415b', 'name': 'notebook1', 'type': 'tree', 'path': 'test14/notebook1', 'mode': '040000'}, {'id': 'e69de29bb2d1d6434b8b29ae775ad8c2e48c5391', 'name': 'normal.ipynb', 'type': 'blob', 'path': 'test14/normal.ipynb', 'mode': '100644'}, {'id': 'ffa1d69794ec6093482603da9282c56d62255e49', 'name': 'test.py', 'type': 'blob', 'path': 'test14/test.py', 'mode': '100644'}]
path = "/app/mosaic_version_control/clients/FilesDownloadZip"
import base64
def downloading_folder_contents(repo_name, os_path, path, branch):
    get_file_list = [{'id': 'f3287f557cc556ffaa8322eeb2af9c7a3cf56320', 'name': 'f2', 'type': 'tree', 'path': 'test14/f2', 'mode': '040000'}, {'id': '38363baaf368da00caa349345186800059f12334', 'name': 'inside_14', 'type': 'tree', 'path': 'test14/inside_14', 'mode': '040000'}, {'id': '205190ef0a5bd9a6ee2fa7045406b44bce1f7dde', 'name': 'normal', 'type': 'tree', 'path': 'test14/normal', 'mode': '040000'}, {'id': '9f38eff59aa981d6b596e5fd3e54aceb84dc415b', 'name': 'notebook1', 'type': 'tree', 'path': 'test14/notebook1', 'mode': '040000'}, {'id': 'e69de29bb2d1d6434b8b29ae775ad8c2e48c5391', 'name': 'normal.ipynb', 'type': 'blob', 'path': 'test14/normal.ipynb', 'mode': '100644'}, {'id': 'ffa1d69794ec6093482603da9282c56d62255e49', 'name': 'test.py', 'type': 'blob', 'path': 'test14/test.py', 'mode': '100644'}]
    path = "/app/mosaic_version_control/clients/FilesDownloadZip"

    for file in get_file_list:
        if file['type'] == 'blob':
            print('IN BLOB')
            print(file['name'])
            #read_json = self.read_file(repo_name, file['path'], branch)
            read_json = ""
            print(read_json)
            # # content = read_json["content"]
            # # content_decoded = base64.decodebytes(content.encode())
            # with open(path + "/" + file['name'], "wb") as binary_file:
            #     # Write bytes to file
            #     binary_file.write(content_decoded)
            # binary_file.close()

    for file in get_file_list:
        if file['type'] == 'tree':
            print('IN TREE')
            path = path + '/' + file['name']
            print(path)
            Path(path).mkdir(parents=True, exist_ok=True)
            downloading_folder_contents(repo_name, file['path'], path, branch)
downloading_folder_contents(repo_name, file_path, path, branch)