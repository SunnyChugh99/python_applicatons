import models
g: "_AppCtxGlobals" = LocalProxy(partial(_lookup_app_object, "g"))  # type: ignore


deployment_id = "74a5aa74-8793-4e50-8c75-d4cb72d21bcc"
ml_model_id = "ef0afa79-f6d0-4308-9b68-d627ca94f6d7"
deployment = g.db_session.query(models.MLModelDeployment).get(deployment_id)
deployment_info = deployment.deployment_info


model_details = g.db_session.query(models.MLModel).get(ml_model_id)
deployment_details = fetch_deployment_details(
    deployment_info["deployment_type"], model_details.type
)