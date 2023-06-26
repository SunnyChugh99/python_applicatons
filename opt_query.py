def get_model_version_data(all_filters, page, per_page):
    count_query = g.db_session.query(MLModelDeployment.ml_model_id, func.count(MLModelDeployment.ml_model_id).label("deployed_count"))\
        .filter( MLModelDeployment.deployment_status == DeploymentStatus.Deployed).group_by(MLModelDeployment.ml_model_id).subquery()
    print(count_query)
    print('PRINTING SUB-1')
    subquery = g.db_session.query(models.MLModelVersion.ml_model_id).outerjoin(models.MLModelDeployment,
                                                                               models.MLModelVersion.id == models.MLModelDeployment.version_id).outerjoin(
        models.MLModel, models.MLModel.id == models.MLModelVersion.ml_model_id).filter(*all_filters).group_by(
        models.MLModelVersion.ml_model_id).order_by(func.max(models.MLModelVersion.created_on).desc()).paginate(page, per_page)
    print(subquery)
    model_ids = subquery.items
    pagination_data = get_pagination_data(subquery)
    ml_ids = [ele[0] for ele in model_ids if ele[0]]
    all_filters.append(models.MLModel.id.in_(ml_ids))
    #Main query to fetch the model data for the specified model IDs
    model_version_list = g.db_session.query(models.MLModelVersion, models.MLModelDeployment, models.MLModel,
                                            count_query.c.deployed_count).outerjoin(models.MLModelDeployment,
                                                                                    models.MLModelVersion.id == models.MLModelDeployment.version_id).outerjoin(
        models.MLModel, models.MLModel.id == models.MLModelVersion.ml_model_id).outerjoin(count_query,
                                                                                          count_query.c.ml_model_id == models.MLModel.id).filter(
        *all_filters).order_by(models.MLModelVersion.created_on.desc()).all()

    print('printing final query')
    print(model_version_list)
    return model_version_list, pagination_data


def get_pagination_data(pagination_object):
    return {'page': pagination_object.page, 'per_page': pagination_object.per_page,
            'pages': pagination_object.pages, 'has_next': pagination_object.has_next,
            'has_prev': pagination_object.has_prev, 'total': pagination_object.total}
