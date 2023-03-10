# -*- coding: utf-8 -*-

import tempfile
import os
#import request
os.environ['R_HOME'] = "/opt/miniconda/lib/R"


def load_model(model_path):
    readRDS = robjects.r["readRDS"]
    return readRDS(model_path)



def uuid_generator():
    _uuid = uuid4()
    return str(_uuid)


def load_r_packages(package_list):
    print('1aas1111')
    from rpy2.robjects import r
    import rpy2.robjects as robjects
    import rpy2.robjects.packages as rpackages
    if package_list:
        package_list = f"('{package_list[0]}')" if len(package_list) == 1 else tuple(package_list)
        load_func = f"""function(){{
                        packages <- c{package_list}
                        for (package in packages){{
                            library(package, character.only = TRUE)
                        }}}}"""
        try:
            robjects.r(load_func)()
            print('Successfully loaded packages')
        except Exception as ex:
            print('Error while loading packages: ', ex)

p_list = ['rJava']
load_r_packages(p_list)






# -*- coding: utf-8 -*-
import shutil


import tempfile
import os
#import request

def load_model(model_path):
    from rpy2.robjects import r
    import rpy2.robjects as robjects
    import rpy2.robjects.packages as rpackages
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
#/tmp/RtmpiTrRha/motmpdel.rds

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
scoring_func_file = "/tmp/RtmpBouVAa/score.rds"
model_file = "/tmp/RtmpBouVAa/model.rds"
model = load_model(model_file)
scoring = load_model(scoring_func_file)
response = scoring(model, "/notebooks/notebooks/train.csv")
print(response)
shutil.rmtree(temp_file)
r.write(response, file=file_temp)
print("5")
