# -*- coding: utf-8 -*-
import rpy2.robjects.packages as rpackages

def load_r_packages(package_list):
    print('1aas1111')
    for package in package_list:
        rpackages.importr(package, on_conflict="warn")


p_list = ['rJava']
load_r_packages(p_list)
