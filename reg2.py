url = "https://dev.refract-fosfor.com/registry/api/v1/model/register/tarball"
f = open(settings.filepath + modelfilename, 'rb')
payload = {
"tar_file": (modelfilename, f, "application/gzip"),
"base_id": "3.6",
"flavour": "sklearn",
"name": "test123Swag1",
"description": "test123"
}




headers_data = {"Authorization": "Bearer " + generate_token(), "Content-Type": multipart_data.content_type,  "X-Project-Id": projectid}