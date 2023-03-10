# -*- coding: utf-8 -*-
import rpy2.robjects as robjects

print('11111')
def check_pre_installed_packages(packages_list, version_list, cran_package_list):
    packages = []
    print('11111')
    for i, package in enumerate(packages_list):
        if package not in cran_package_list:
            packages.append({"name": package, "version": version_list[i]})

    if len(packages) == 0:
        packages.append({"name": "devtools", "version": "2.3.2"})
        packages.append({"name": "versions", "version": "0.3"})

    return packages


print('11sa1112113')
def load_r_packages(package_list):
    print('1aas1111')
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

def get_r_packages():
    try:
        print('1111ssa1')
        fetch_package_name = """
            function(){
                packages <- installed.packages()
                df <- data.frame(packages)
                package_name <- sapply(df$Package, as.character)
                return(package_name)
            }
        """
        fetch_version_name = """
            function(){
                packages <- installed.packages()
                df <- data.frame(packages)
                package_version <- sapply(df$Version, as.character)
                return(package_version)
            }
        """
        package_name_r = robjects.r(fetch_package_name)
        version_name_r = robjects.r(fetch_version_name)

        packages = package_name_r()
        versions = version_name_r()
        package_list = list(packages)
        version_list = list(versions)
        return package_list, version_list

    except Exception as e:
        print('EXCEPT')

print('10')
package_list, version_list = get_r_packages()
print('11')
cran_package_list = [
        "base",
        "boot",
        "class",
        "cluster",
        "codetools",
        "compiler",
        "datasets",
        "evaluate",
        "foreign",
        "graphics",
        "grDevices",
        "grid",
        "IRkernel",
        "KernSmooth",
        "lattice",
        "MASS",
        "Matrix",
        "methods",
        "mgcv",
        "mosaicrml",
        "nlme",
        "nnet",
        "parallel",
        "pbdZMQ",
        "compareDF",
        "rlang",
        "rpart",
        "spatial",
        "splines",
        "stats",
        "stats4",
        "survival",
        "tcltk",
        "tools",
        "utils",
    ]

pkg_list = check_pre_installed_packages(
    package_list, version_list, cran_package_list
)
print('11')
p_list = [package["name"] for package in pkg_list]
print("PAKCA")
print(p_list)
print("Starting - loading of packages")
load_r_packages(p_list)
print("Packages loaded successfully")