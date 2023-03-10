def get(self,
        pod_name: str,
        container_name: str) -> Tuple[Any, int]:
    """
    This method will fetch all the logs from the log central container
    :param pod_name: Name of the kubernetes pod
    :param container_name: Name of container to stream logs
    :return: Dict[python_packages]
    """

    self.pod_name = pod_name
    self.container_name = container_name
    self.namespace = app.config["KUBERNETES_NAMESPACE"]
    _total_py_package = 0
    _total_r_package = 0
    exhaustive_pkg_df = None

    print(f"FetchPackageView: {self.pod_name} - {self.container_name}")
    try:
        cmd_r = """\"ip <- as.data.frame(installed.packages()[,c(1,3)])
           write.table(ip, sep = '==',row.names = FALSE)\""""

        pkg_commands = ["pip freeze",
                        ('echo {} > get_package.R \n'
                         'Rscript get_package.R \n'
                         .format(cmd_r))]
        pkg_kernel = ["Python", "R"]
        for each_command, each_kernel in zip(pkg_commands, pkg_kernel):
            try:
                pkg_raw = self.exec(each_command)
                pkg_frame = pd.read_csv(io.StringIO(pkg_raw),
                                        header=None,
                                        names=["package_name"])
                print(f"DF :: {pkg_frame}")
                pkg_frame[['pkg',
                           'version']] = pkg_frame.package_name.str.split("==",
                                                                          expand=True)
                pkg_frame.drop(["package_name"], inplace=True, axis=1)
                pkg_frame['type'] = each_kernel

                if exhaustive_pkg_df is not None:
                    exhaustive_pkg_df = exhaustive_pkg_df.append(pkg_frame)
                else:
                    exhaustive_pkg_df = pkg_frame
            # pylint: disable=broad-except
            except Exception as e:
                msg_ = "FetchPackageView: Unsupported {} {}".format(each_kernel,
                                                                    str(e))
                current_app.logger.warn(msg_)
                current_app.logger.error(str(traceback.format_exc()))

        python_pkg_json = exhaustive_pkg_df.to_json(orient='records')
        _total_py_package = exhaustive_pkg_df[exhaustive_pkg_df["type"] == "Python"].shape[0]
        _total_r_package = exhaustive_pkg_df[exhaustive_pkg_df["type"] == "R"].shape[0]
    # pylint: disable=broad-except
    except Exception as e:
        python_pkg_json = "{}"
        current_app.logger.warn("FetchPackageView: {}".format(str(e)))
        current_app.logger.error(str(traceback.format_exc()))

    return jsonify(packages=json.loads(python_pkg_json),
                   total_py_package=_total_py_package,
                   total_r_package=_total_r_package
                   ), 200

