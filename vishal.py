def register_model(projectid, modelname, description, modelfilename, flavour):
    f = open(settings.filepath + modelfilename, 'rb')

    payload = {
        "tar_file": (modelfilename, f, "application/gzip"),
        "base_id": "3.6",
        "flavour": flavour,
        "name": modelname,
        "description": description
    }

    multipart_data = MultipartEncoder(fields=payload)

    headers_data = {"Authorization": "Bearer " + generate_token(), "Content-Type": multipart_data.content_type,
     "X-Project-Id": projectid}
    url = settings.baseurl + settings.modelapi + settings.modelcontextpath
    response = requests.post(
    url=url,
    data=multipart_data,
    headers=headers_data, verify=False)
    print("register_model url:", response.url)
    print("register_model status_code:", response.status_code)
    return response.text