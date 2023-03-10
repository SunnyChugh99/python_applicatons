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

tree_list = [{'id': '20bb56f0a4d514349ae52e15866b64e1fbd97d2c', 'name': '?', 'type': 'tree', 'path': 'test12/?', 'mode': '040000'},
 {'id': '2a5e5975e4f165f9a205d31598d003ee6617f676', 'name': 'inside_12', 'type': 'tree', 'path': 'test12/inside_12',
  'mode': '040000'},
 {'id': '9f38eff59aa981d6b596e5fd3e54aceb84dc415b', 'name': 'notebook1', 'type': 'tree', 'path': 'test12/notebook1',
  'mode': '040000'},
 {'id': 'ffa1d69794ec6093482603da9282c56d62255e49', 'name': 'test.py', 'type': 'blob', 'path': 'test12/test.py',
  'mode': '100644'}]

def downloading_folder_contents(repo_name, file_path, folderpath, branch="master"):
    """
    downloads folder content with structure
    :param repo_name:
    :param file_path:
    :param folderpath:
    :param branch:
    :return:
    """
    print('Inside nested-1')
    print(repo_name)
    print(file_path)
    print(folderpath)
    print(branch)
    print('Inside nested-2')
    #get_file_list = self.list_files(repo_name, file_path, branch)
    print('LISTING FILES-1')

    get_file_list = ['']
    print(get_file_list)
    print('LISTING FILES-2')
    path = folderpath
    for file in get_file_list:
        if file['type'] == 'blob':
            print('IN BLOB')
            read_json = self.read_file(repo_name, file['path'], branch)
            print(read_json)
            content = read_json["content"]
            content_decoded = base64.decodebytes(content.encode())
            with open(path + "/" + file['name'], "wb") as binary_file:
                # Write bytes to file
                binary_file.write(content_decoded)
            binary_file.close()

    for file in get_file_list:
        if file['type'] == 'tree':
            print('IN TREE')
            path = path + '/' + file['name']
            print(path)
            Path(path).mkdir(parents=True, exist_ok=True)
            downloading_folder_contents(repo_name, file['path'], path, branch)

def download_folder(repo_url, repo_name, file_path, branch="master"):
    """
    downloads file
    :param file_path
    :param repo_name
    :param branch
    :return:
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    folder_name = file_path.split('/')[-1]
    folderpath = dir_path + '/FilesDownloadZip/' + folder_name
    Path(folderpath).mkdir(parents=True, exist_ok=True)
    repo_name = repo_url
    downloading_folder_contents(repo_name, file_path, folderpath, branch)
    # initializing empty file paths list
    file_paths = []
    zip_folder_dir = dir_path + '/FilesDownloadZip'
    os.chdir(zip_folder_dir)

    # crawling through directory and subdirectories
    for root, directories, files in os.walk(f'./{folder_name}'):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)


    # writing files to a zipfile
    with ZipFile(folder_name + '.zip', 'w') as zip:
        # writing each file one by one
        for file in file_paths:
            zip.write(file)

    resp = open(folder_name + '.zip', 'rb')
    os.remove(folder_name + '.zip')
    shutil.rmtree(folder_name)


    return 1

if isfolder == "true":
   a = download_folder(repo_url,repo_name, file_path, branch)
else:
    #response = client.download_file(repo_url, file_path, branch)
    file_name = file_path.split('/')[-1]


