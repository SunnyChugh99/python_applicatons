def get_model_version_data(all_filters,  page, per_page):


    # alerts = alert_query.limit(per_page).offset((page - 1) * per_page).all()
    # total_pages = ceil(total_alerts / per_page)
    # # Paginate query
    # alerts = alert_query.limit(per_page).offset((page - 1) * per_page).all()
    #

    count_query = g.db_session.query(MLModelDeployment.ml_model_id, func.count(MLModelDeployment.ml_model_id).label("deployed_count")).filter(
        MLModelDeployment.deployment_status == DeploymentStatus.Deployed).group_by(MLModelDeployment.ml_model_id).subquery()
    from sqlalchemy import func as sql_func, and_

    subquery = g.db_session.query(models.MLModelVersion.ml_model_id) \
        .group_by(models.MLModelVersion.ml_model_id) \
        .order_by(sql_func.max(models.MLModelVersion.created_on).desc()) \
        .limit(per_page).offset((page - 1) * per_page) \
        .subquery()

    # Main query to fetch the model data for the specified model IDs
    model_version_list = g.db_session.query(models.MLModelVersion, models.MLModelDeployment, models.MLModel,
                                            count_query.c.deployed_count) \
        .outerjoin(models.MLModelDeployment, models.MLModelVersion.id == models.MLModelDeployment.version_id) \
        .outerjoin(models.MLModel, models.MLModel.id == models.MLModelVersion.ml_model_id) \
        .outerjoin(count_query, count_query.c.ml_model_id == models.MLModel.id) \
        .join(subquery, models.MLModelVersion.ml_model_id == subquery.c.ml_model_id) \
        .filter(*all_filters).order_by(models.MLModelVersion.created_on.desc()).all()

    return model_version_list


model_version_list = get_model_version_data(all_filters, page, per_page)
model_data = OrderedDict()
for model_version in model_version_list:
    print(model_version)
    model_id = model_version.MLModelVersion.ml_model_id

    if model_id not in model_data:
        model_data[model_id] = {
            "versions": [],
            "model_name": model_version.MLModel.name,
            "model_id": model_id,
            "outside_refract": model_version.MLModel.outside_refract,
            "deployed_count": model_version.deployed_count
        }

    version_data = {
        "version": model_version.MLModelVersion.id,
        "created_by": model_version.MLModelVersion.created_by,
        "created_date": model_version.MLModelVersion.created_on.strftime("%a, %d %b %Y %H:%M:%S GMT"),
        "validation_report": model_version.MLModelVersion.validation_report,
        "reviewed": model_version.MLModelVersion.reviewed_flag,
        # "dataset_used": model_version.MLModelVersion.dataset_used,
        "model_status": model_version.MLModelDeployment.deployment_status,
        "project_id": model_version.MLModel.project_id,
        "version_id": model_version.MLModelVersion.id,
        # "kernal_type": model_version.MLModelVersion.kernal_type
    }

    model_data[model_id]["versions"].append(version_data)

