import os
def check_and_create_directory(path):
    """
    Checking if folder exist if folder is not exist then it will create the folders
    :param path
    :return:file_path
    """
    path_array = path.split("/")
    directory = "/"
    for split_path in path_array:
        directory = directory + split_path + "/"
        if not os.path.isdir(directory):
            os.mkdir(directory, 0o777)
    os.chmod(path, 0o777)
    return "Folder created successfully!"

def check_and_create_log_directory(path):
    """
    Checking if folder exist if folder is not exist then it will create the folders
    :param path
    :return:file_path
    """
    path_array = path.split("/")
    directory = "/"
    for split_path in path_array:
        directory = directory + split_path + "/"
        if not os.path.isdir(directory):
            os.mkdir(directory, 0o777)
    package_file_path = path + 'package-installation.log'
    init_script_path = path + 'init-script.log'
    if os.path.exists(package_file_path):
        os.remove(package_file_path)
    if os.path.exists(init_script_path):
        os.remove(init_script_path)

    os.chmod(path, 0o777)
    return "Folder created successfully!"



NOTEBOOK_MOUNT_PATH="/sandbox_shared/logistics/notebooks/"
MINIO_DATA_BUCKET = "mosaic-scb-test"
project_id = "2d8b6cca-66f8-4211-8221-8c9aaad02562"

snaphot_path = NOTEBOOK_MOUNT_PATH + MINIO_DATA_BUCKET + "/" + f'{project_id}/{project_id}-Snapshot/123/'

check_and_create_directory(snaphot_path)

log_path = NOTEBOOK_MOUNT_PATH + MINIO_DATA_BUCKET + "/" + "log/" + f'{project_id}' + "/" + '123432' + "/"
check_and_create_log_directory(log_path)