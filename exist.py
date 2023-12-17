def register_model(projectid, modelname, description, modelfilename, flavour):
    f = open(settings.filepath + modelfilename, 'rb')
    payload = {
        "tar_file": (modelfilename, f, "application/gzip"),
        "base_id": "3.6",
        "flavour": "sklearn",
        "name": "test123Swag1",
        "description": "test123"
    }
    multipart_data = MultipartEncoder(fields={'tar_file': (modelfilename, f), })
    headers_data = {"Authorization": "Bearer " + generate_token(), "Content-Type": multipart_data.content_type, "X-Project-Id": projectid}
    url = settings.baseurl + settings.modelapi + settings.modelcontextpath + "name=" + modelname + "&" + "description=" + description + "&" + flavour
    response = requests.post(
    url=url,
    data=multipart_data,
    headers=headers_data, verify=False)
    print("register_model url:", response.url)
    print("register_model status_code:", response.status_code)

    return response.text