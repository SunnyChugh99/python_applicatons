import requests

url = "http://localhost:5000/registry/api/v1/model/register/tarball"
payload = {
    "base_id": "3.6",
    "flavour": "sklearn",
    "name": "test123Swag32323",
    "description": "test123"
}
files = {
    "tar_file": ("fifa_model_proper.tar.gz", open("fifa_model_proper.tar.gz", "rb"), "application/gzip"),
}

headers = {
    "AUTHORIZATION": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJ4WTdTd3k5UE1xaXRDQmNSMm5qcVl6bmoxS3NqZzV3TmdOV0xDVzdyUkhvIn0.eyJleHAiOjE2ODExMTQ5MDksImlhdCI6MTY4MTExMzEwOSwianRpIjoiZmUwMzhlNDQtYTEwYy00ZTU4LTg5OTItMjliNTRhYTk0MjQ3IiwiaXNzIjoiaHR0cHM6Ly9kZXYtYXV0aC5yZWZyYWN0LWZvc2Zvci5jb20vYXV0aC9yZWFsbXMvbW9zYWljIiwiYXVkIjpbIm1vc2FpYy1nYXRla2VlcGVyIiwiYWNjb3VudCJdLCJzdWIiOiIzN2U0ZGE0Yy02NmEyLTQyMzAtYTJmNC1iMGE4NTVhNWJhMWUiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJtb3NhaWMtZ2F0ZWtlZXBlciIsInNlc3Npb25fc3RhdGUiOiJmZmM3Mzc1MS1kZmI3LTRiYTItYjQ0Mi1hOTEyNGM0NDUzOTUiLCJhbGxvd2VkLW9yaWdpbnMiOlsiKiJdLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsiTUxPUFMiLCJzcGVjdHJhLWRldmVsb3BlciIsInJlZnJhY3QtZGV2ZWxvcGVyIiwib2ZmbGluZV9hY2Nlc3MiLCJhZG1pbiIsInVtYV9hdXRob3JpemF0aW9uIiwicmVmcmFjdC1hZG1pbiJdfSwicmVzb3VyY2VfYWNjZXNzIjp7ImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoiZ3JvdXBzIHRlc3QgZW1haWwgdXNlcl9hdHRyaWJ1dGUgcHJvZmlsZSIsInNpZCI6ImZmYzczNzUxLWRmYjctNGJhMi1iNDQyLWE5MTI0YzQ0NTM5NSIsImFhdmVzIjpbIk1MT1BTIiwic3BlY3RyYS1kZXZlbG9wZXIiLCJyZWZyYWN0LWRldmVsb3BlciIsIm9mZmxpbmVfYWNjZXNzIiwiYWRtaW4iLCJ1bWFfYXV0aG9yaXphdGlvbiIsInJlZnJhY3QtYWRtaW4iXSwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJ0ZXN0IjpbIk1MT1BTIiwic3BlY3RyYS1kZXZlbG9wZXIiLCJyZWZyYWN0LWRldmVsb3BlciIsIm9mZmxpbmVfYWNjZXNzIiwiYWRtaW4iLCJ1bWFfYXV0aG9yaXphdGlvbiIsInJlZnJhY3QtYWRtaW4iXSwibmFtZSI6IlJlZnJhY3QgQWRtaW4iLCJncm91cHMiOlsiTUxPUFMiLCJzcGVjdHJhLWRldmVsb3BlciIsInJlZnJhY3QtZGV2ZWxvcGVyIiwib2ZmbGluZV9hY2Nlc3MiLCJhZG1pbiIsInVtYV9hdXRob3JpemF0aW9uIiwicmVmcmFjdC1hZG1pbiJdLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJyZWZyYWN0LmFkbWluIiwiZ2l2ZW5fbmFtZSI6IlJlZnJhY3QiLCJmYW1pbHlfbmFtZSI6IkFkbWluIiwiZW1haWwiOiJyZWZyYWN0LmFkbWluQGZvc2Zvci5jb20ifQ.PD4tJ7dNACl8n3qEzyfezT4HYDGQ0h2giP9__3iDXh1zFSREaDKCop8ctu3YANjSErrDYR4tpTetMVEEZSYfpKD2jxtfIgzhSk-Qn_3is_toxI82YvvrC-XwlK5YrgVmhefAgUCWfSuX91yLHFlgYTgHp7wvcv63os5tzru9cXISS6C_3tJURptSMjYC1Q1mBIsFnoR3eq_vdgaZdEE4rB6dinTjzmivIm08f6ggGhv4Dn8RNBRrpFrnyTw3KH1QkwqDzRNDAuZ5r_9kZ5s8s23SE48Lgfz76Y50ff2JQsecy7RYAEQq17y3C6rbkRfMrpHZTAbSrC8529B938nntg",
    "accept": "application/json",
    "X-Project-Id": "af74ae22-cc77-4a24-96ee-1a72d295b4db"
}
response = requests.post(url, headers=headers, data=payload, files=files)

print(response.text)


