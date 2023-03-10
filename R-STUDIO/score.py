# -*- coding: utf-8 -*-
import shutil

import rpy2.robjects as robjects


from rpy2.robjects import r

import tempfile
import os
#import request

def load_model(model_path):
    readRDS = robjects.r["readRDS"]
    return readRDS(model_path)


#
# def uuid_generator():
#     _uuid = uuid4()
#     return str(_uuid)
#







#SCORE
#/tmp/RtmpYaKgn9

#model.rds
#repos_https%3A%2F%2Fmran.microsoft.com%2Fsnapshot%2F2019-12-06%2Fsrc%2Fcontrib.rds
#score.rds
#/tmp/RtmpiTrRha/model.rds

print("1")
response_temp = tempfile.mkdtemp() + "/"
file_temp = response_temp + "1233" + ".txt"
print("2")
#file = request.files.get("file1")
temp_file = tempfile.mkdtemp()
#file.save(os.path.join(temp_file, file.filename))

print("3")
tmp_file_path = os.path.join(temp_file, "/notebooks/notebooks/test.py")
print("4")
scoring_func_file = "/tmp/RtmpaehXjd/score.rds"
model_file = "/tmp/RtmpaehXjd/model.rds"
model = load_model(model_file)
scoring = load_model(scoring_func_file)
response = scoring(model, "train.csv")
print(response)
shutil.rmtree(temp_file)
r.write(response, file=file_temp)
print("5")
