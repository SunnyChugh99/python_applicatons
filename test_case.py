#!/usr/bin/env python
# -*- coding: utf-8 -*-
import http.server
import os
import socketserver
import subprocess
import sys
import shutil
from datetime import datetime
import uuid

import click

import alembic.config

from flask.cli import FlaskGroup
from sqlalchemy import create_engine
from mosaic.ai import application, db
from mosaic.ai.config import config
from mosaic.ai.models import Base
from mosaic_utils.ai.k8.pod_metrics_summary import fetch_resource_limitscaling_guarantee

session = db.session


def app_factory():
    """ App method """
    return application


@click.group(cls=FlaskGroup, create_app=app_factory)
def cli():
    """ CLI for mosaic-ai-backend """


def insert_docker(docker_image_url):
    """ insert docker image id """

    from mosaic.ai.models import MLModelVersion

    version_record = session.query(MLModelVersion).all()
    for version in version_record:
        if version.docker_image_url is None:
            version.docker_image_url = docker_image_url
            session.add(version)
            session.flush()

    session.commit()


def create_resource_data():
    """ create tables in the database """
    from mosaic.ai.models import MLModelResource

    resources = {
        "Micro": {
            "min_replicas": "1",
            "max_replicas": "3",
            "cpu_limit": "500m",
            "ram_limit": "300Mi",
            "gpu_type": "cpu",
            "status": "ENABLED",
        },
        "mini": {
            "min_replicas": "1",
            "max_replicas": "3",
            "cpu_limit": "800m",
            "ram_limit": "500Mi",
            "gpu_type": "cpu",
            "status": "ENABLED",
        },
        "default": {
            "min_replicas": "1",
            "max_replicas": "3",
            "cpu_limit": "1",
            "ram_limit": "800Mi",
            "gpu_type": "cpu",
            "status": "ENABLED",
        },
        "Small": {
            "min_replicas": "1",
            "max_replicas": "3",
            "cpu_limit": "1",
            "ram_limit": "2Gi",
            "gpu_type": "cpu",
            "status": "ENABLED",
        },
        "Medium": {
            "min_replicas": "1",
            "max_replicas": "3",
            "cpu_limit": "2",
            "ram_limit": "4Gi",
            "gpu_type": "cpu",
            "status": "ENABLED",
        },
        "large": {
            "min_replicas": "1",
            "max_replicas": "3",
            "cpu_limit": "2",
            "ram_limit": "8Gi",
            "gpu_type": "cpu",
            "status": "ENABLED",
        },
        "XLarge": {
            "min_replicas": "1",
            "max_replicas": "3",
            "cpu_limit": "4",
            "ram_limit": "16Gi",
            "gpu_type": "cpu",
            "status": "ENABLED",
        },
        "2XLarge": {
            "min_replicas": "1",
            "max_replicas": "3",
            "cpu_limit": "8",
            "ram_limit": "32Gi",
            "gpu_type": "cpu",
            "status": "ENABLED",
        },
        "GPU-Nvidia-Small": {
            "min_replicas": "1",
            "max_replicas": "3",
            "cpu_request": "1",
            "cpu_limit": "1",
            "ram_request": "300Mi",
            "ram_limit": "32Gi",
            "gpu_type": "nvidia",
            "status": "ENABLED",
        },
        "GPU-Nvidia-Medium": {
            "min_replicas": "1",
            "max_replicas": "3",
            "cpu_request": "2",
            "cpu_limit": "2",
            "ram_request": "300Mi",
            "ram_limit": "32Gi",
            "gpu_type": "nvidia",
            "status": "ENABLED",
        },
        "GPU-Nvidia-Large": {
            "min_replicas": "1",
            "max_replicas": "3",
            "cpu_request": "4",
            "cpu_limit": "4",
            "ram_request": "300Mi",
            "ram_limit": "32Gi",
            "gpu_type": "nvidia",
            "status": "ENABLED",
        },
        "GPU-AMD-Small": {
            "min_replicas": "1",
            "max_replicas": "3",
            "cpu_request": "1",
            "cpu_limit": "1",
            "ram_request": "300Mi",
            "ram_limit": "32Gi",
            "gpu_type": "amd",
            "status": "ENABLED",
        },
        "GPU-AMD-Medium": {
            "min_replicas": "1",
            "max_replicas": "3",
            "cpu_request": "2",
            "cpu_limit": "2",
            "ram_request": "300Mi",
            "ram_limit": "32Gi",
            "gpu_type": "amd",
            "status": "ENABLED",
        },
        "GPU-AMD-Large": {
            "min_replicas": "1",
            "max_replicas": "3",
            "cpu_request": "4",
            "cpu_limit": "4",
            "ram_request": "300Mi",
            "ram_limit": "32Gi",
            "gpu_type": "amd",
            "status": "ENABLED",
        },
    }
    for name in resources:
        record = (
            session.query(MLModelResource).filter(MLModelResource.name == name).first()
        )
        resource_extra = ""
        # request percentage is kept -25 as we want request to be 75% of limit
        if record is None:
            resource = MLModelResource()
            resource.name = name
            resource.cpu_limit = resources[name]["cpu_limit"]
            resource.ram_limit = resources[name]["ram_limit"]
            print('1')
            print(config.get("deployment_request_config", "request_percentage"))
            limit_cpu_mem = fetch_resource_limitscaling_guarantee(
                resource.cpu_limit,
                resource.ram_limit,
                resource_extra,
                config.get("deployment_request_config", "request_percentage")
            )
            resource.cpu_request = limit_cpu_mem["cpu"]
            resource.ram_request = limit_cpu_mem["memory"]
            resource.min_replicas = resources[name]["min_replicas"]
            resource.max_replicas = resources[name]["max_replicas"]
            resource.gpu_type = resources[name]["gpu_type"]
            resource.status = resources[name]["status"]
            session.add(resource)
            session.flush()
        else:
            # update data
            cpu = getattr(record, "cpu_limit")
            mem = getattr(record, "ram_limit")
            print('2')
            print(config.get("deployment_request_config", "request_percentage"))
            limit_cpu_mem = fetch_resource_limitscaling_guarantee(
                cpu,
                mem,
                resource_extra,
                config.get("deployment_request_config", "request_percentage"),
                1
            )
            setattr(record, "cpu_request", limit_cpu_mem["cpu"])
            setattr(record, "ram_request", limit_cpu_mem["memory"])

            for key, val in resources[name].items():
                setattr(record, key, val)
            session.add(record)
            session.flush()

    session.commit()


images = {
    "Python": {
        "id": str(uuid.uuid4()),
        "created_by": "System",
        "created_on": datetime.now(),
        "last_modified_by": "System",
        "last_modified_on": datetime.now(),
        "type": "PRE_BUILD",
        "description": "python",
        "docker_url": "{}/mosaic-ai-logistics/mosaic-notebooks-manager/dash-app-serving:1.1.0".format(
            config.get("docker-registry", "docker_registry_path")),
        "gpu_docker_url": "{}/mosaic-ai-logistics/mosaic-notebooks-manager/dash-app-serving:1.0.3".format(
            config.get("docker-registry", "docker_registry_path")),
        "category": "APPLICATION"
    },
    "Java": {
        "id": str(uuid.uuid4()),
        "created_by": "System",
        "created_on": datetime.now(),
        "last_modified_by": "System",
        "last_modified_on": datetime.now(),
        "type": "PRE_BUILD",
        "description": "java",
        "docker_url": "{}/mosaic-ai-logistics/mosaic-notebooks-manager/app-serving:1.1.15".format(
            config.get("docker-registry", "docker_registry_path")),
        "gpu_docker_url": "{}/mosaic-ai-logistics/mosaic-notebooks-manager/app-serving:gpu-1.1.10".format(
            config.get("docker-registry", "docker_registry_path")),
        "category": "APPLICATION"
    },
    "Model": {
        "id": str(uuid.uuid4()),
        "created_by": "System",
        "created_on": datetime.now(),
        "last_modified_by": "System",
        "last_modified_on": datetime.now(),
        "type": "CUSTOM_BUILD",
        "description": "model",
        "docker_url": "{}/mosaic-ai-logistics/mosaic-notebooks-manager/jupyter/3.6:2.6.13".format(config.get("docker-registry", "docker_registry_path")),
        "gpu_docker_url": "{}/mosaic-ai-logistics/mosaic-notebooks-manager/jupyter/3.6:2.6.13".format(config.get("docker-registry", "docker_registry_path")),
        "category": "MODEL"
    },
    "Model3.7": {
        "id": str(uuid.uuid4()),
        "created_by": "System",
        "created_on": datetime.now(),
        "last_modified_by": "System",
        "last_modified_on": datetime.now(),
        "type": "CUSTOM_BUILD",
        "description": "model3.7",
        "docker_url": "{}/mosaic-ai-logistics/mosaic-notebooks-manager/jupyter/3.7:3.7V1.19".format(config.get("docker-registry", "docker_registry_path")),
        "gpu_docker_url": "{}/mosaic-ai-logistics/mosaic-notebooks-manager/jupyter/3.7:3.7V1.19".format(config.get("docker-registry", "docker_registry_path")),
        "category": "MODEL"
    },
    "Model3.8": {
        "id": str(uuid.uuid4()),
        "created_by": "System",
        "created_on": datetime.now(),
        "last_modified_by": "System",
        "last_modified_on": datetime.now(),
        "type": "CUSTOM_BUILD",
        "description": "model3.8",
        "docker_url": "{}/mosaic-ai-logistics/mosaic-notebooks-manager/jupyter/3.8:3.8V1.0.4_Non_Vanilla_04".format(config.get("docker-registry", "docker_registry_path")),
        "gpu_docker_url": "{}/mosaic-ai-logistics/mosaic-notebooks-manager/jupyter/3.8:3.8V1.0.4_Non_Vanilla_04".format(config.get("docker-registry", "docker_registry_path")),
        "category": "MODEL"
    },
    "Model3.9": {
        "id": str(uuid.uuid4()),
        "created_by": "System",
        "created_on": datetime.now(),
        "last_modified_by": "System",
        "last_modified_on": datetime.now(),
        "type": "CUSTOM_BUILD",
        "description": "model3.9",
        "docker_url": "{}/mosaic-ai-logistics/mosaic-notebooks-manager/jupyter/3.9:3.9_non_vanilla_V1.1.5".format(
            config.get("docker-registry", "docker_registry_path")),
        "gpu_docker_url": "{}/mosaic-ai-logistics/mosaic-notebooks-manager/jupyter/3.9:3.9_non_vanilla_V1.1.5".format(
            config.get("docker-registry", "docker_registry_path")),
        "category": "MODEL"
    },
    "Model3.10": {
        "id": str(uuid.uuid4()),
        "created_by": "System",
        "created_on": datetime.now(),
        "last_modified_by": "System",
        "last_modified_on": datetime.now(),
        "type": "CUSTOM_BUILD",
        "description": "model3.10",
        "docker_url": "{}/mosaic-ai-logistics/mosaic-notebooks-manager/jupyter/3.10:3.10_non_vanilla_V1.0.2".format(
            config.get("docker-registry", "docker_registry_path")),
        "gpu_docker_url": "{}/mosaic-ai-logistics/mosaic-notebooks-manager/jupyter/3.10:3.10_non_vanilla_V1.0.2".format(
            config.get("docker-registry", "docker_registry_path")),
        "category": "MODEL"
    },
    "RModel": {
        "id": str(uuid.uuid4()),
        "created_by": "System",
        "created_on": datetime.now(),
        "last_modified_by": "System",
        "last_modified_on": datetime.now(),
        "type": "CUSTOM_BUILD",
        "description": "Rmodel",
        "docker_url": "{}/mosaic-ai-logistics/mosaic-ai-serving/r:2.0.14-49-readonly".format(
            config.get("docker-registry", "docker_registry_path")),
        "gpu_docker_url": "{}/mosaic-ai-logistics/mosaic-ai-serving/r:gpu-1.0.0-11".format(
            config.get("docker-registry", "docker_registry_path")),
        "category": "MODEL"
    },
    "RModel4.1": {
        "id": str(uuid.uuid4()),
        "created_by": "System",
        "created_on": datetime.now(),
        "last_modified_by": "System",
        "last_modified_on": datetime.now(),
        "type": "CUSTOM_BUILD",
        "description": "RModel4.1",
        "docker_url": "{}/mosaic-ai-logistics/mosaic-ai-serving/r:2.0.14-49-readonly-4.1".format(config.get("docker-registry", "docker_registry_path")),
        "gpu_docker_url": "{}/mosaic-ai-logistics/mosaic-ai-serving/r:gpu-1.0.0-11".format(config.get("docker-registry", "docker_registry_path")),
        "category": "MODEL"
    },
    "RModelRhel4.1": {
        "id": str(uuid.uuid4()),
        "created_by": "System",
        "created_on": datetime.now(),
        "last_modified_by": "System",
        "last_modified_on": datetime.now(),
        "type": "CUSTOM_BUILD",
        "description": "RModelRhel4.1",
        "docker_url": "{}/mosaic-ai-logistics/mosaic-ai-serving/rstudio_rhl:1.1.20".format(config.get("docker-registry", "docker_registry_path")),
        "gpu_docker_url": "{}/mosaic-ai-logistics/mosaic-ai-serving/rstudio_rhl:1.1.20".format(config.get("docker-registry", "docker_registry_path")),
        "category": "MODEL"
    },
    "Python-Bokeh": {
        "id": str(uuid.uuid4()),
        "created_by": "System",
        "created_on": datetime.now(),
        "last_modified_by": "System",
        "last_modified_on": datetime.now(),
        "type": "PRE_BUILD",
        "description": "bokeh",
        "docker_url": "{}/mosaic-ai-logistics/mosaic-visual-serving:1.0.0-3".format(
            config.get("docker-registry", "docker_registry_path")),
        "gpu_docker_url": "{}/mosaic-ai-logistics/mosaic-visual-serving:gpu-1.0.0-3".format(
            config.get("docker-registry", "docker_registry_path")),
        "category": "APPLICATION"
    },
    "R-Shiny": {
        "id": str(uuid.uuid4()),
        "created_by": "System",
        "created_on": datetime.now(),
        "last_modified_by": "System",
        "last_modified_on": datetime.now(),
        "type": "PRE_BUILD",
        "description": "R-Shiny",
        "docker_url": "{}/mosaic-ai-logistics/mosaic-notebooks-manager/r-shiny-app-serving:1.0.7".format(
            config.get("docker-registry", "docker_registry_path")),
        "gpu_docker_url":
            "{}/mosaic-ai-logistics/mosaic-notebooks-manager/r-shiny-app-serving:1.0.3".format(
                config.get("docker-registry", "docker_registry_path")),
        "category": "APPLICATION"
    },
    "Dash": {
        "id": str(uuid.uuid4()),
        "created_by": "System",
        "created_on": datetime.now(),
        "last_modified_by": "System",
        "last_modified_on": datetime.now(),
        "type": "PRE_BUILD",
        "description": "Dash",
        "docker_url": "{}/mosaic-ai-logistics/mosaic-notebooks-manager/dash-app-serving:1.1.0".format(
            config.get("docker-registry", "docker_registry_path")),
        "gpu_docker_url":
            "{}/mosaic-ai-logistics/mosaic-notebooks-manager/dash-app-serving:1.0.3".format(
                config.get("docker-registry", "docker_registry_path")),
        "category": "APPLICATION"
    },
    "SAS": {
        "id": str(uuid.uuid4()),
        "created_by": "System",
        "created_on": datetime.now(),
        "last_modified_by": "System",
        "last_modified_on": datetime.now(),
        "type": "PRE_BUILD",
        "description": "SAS",
        "docker_url": "{}/mosaic-ai-logistics/mosaic-ai-serving/sas:2.0.10".format(
            config.get("docker-registry", "docker_registry_path")),
        "gpu_docker_url": "",
        "category": "MODEL"
    },
    "KYD_JOBS": {
        "id": str(uuid.uuid4()),
        "created_by": "System",
        "created_on": datetime.now(),
        "last_modified_by": "System",
        "last_modified_on": datetime.now(),
        "type": "PRE_BUILD",
        "description": "KYD_JOBS",
        "docker_url": "{}/mosaic-ai-logistics/mosaic-notebooks-manager/kyd:1.0.2".format(
            config.get("docker-registry", "docker_registry_path")),
        "gpu_docker_url": "{}/mosaic-ai-logistics/mosaic-notebooks-manager/kyd:1.0.2".format(
            config.get("docker-registry", "docker_registry_path")),
        "category": "MODEL"
    },
    "XAI_JOBS": {
        "id": str(uuid.uuid4()),
        "created_by": "System",
        "created_on": datetime.now(),
        "last_modified_by": "System",
        "last_modified_on": datetime.now(),
        "type": "PRE_BUILD",
        "description": "XAI_JOBS",
        "docker_url": "{}/mosaic-ai-logistics/mosaic-notebooks-manager/xai:1.0.2".format(
            config.get("docker-registry", "docker_registry_path")),
        "gpu_docker_url": "{}/mosaic-ai-logistics/mosaic-notebooks-manager/xai:1.0.2".format(
            config.get("docker-registry", "docker_registry_path")),
        "category": "MODEL"
    },
    "Streamlit": {
        "id": str(uuid.uuid4()),
        "created_by": "System",
        "created_on": datetime.now(),
        "last_modified_by": "System",
        "last_modified_on": datetime.now(),
        "type": "PRE_BUILD",
        "description": "Streamlit",
        "docker_url": "{}/mosaic-ai-logistics/mosaic-app-serving/dash_streamlit:1.1.0".format(
            config.get("docker-registry", "docker_registry_path")),
        "gpu_docker_url":
            "{}/mosaic-ai-logistics/mosaic-app-serving/dash_streamlit:1.1.0".format(
                config.get("docker-registry", "docker_registry_path")),
        "category": "APPLICATION"
    }
}


def create_docker_image():
    """ create data for ml_docker_image and ml_model_versions in the database """

    from mosaic.ai.models import MLDockerImage

    for name in images:
        record = session.query(MLDockerImage).filter(MLDockerImage.name == name).first()
        if record is None:
            image = MLDockerImage()
            image.id = images[name]["id"]
            image.name = name
            image.created_by = images[name]["created_by"]
            image.created_on = images[name]["created_on"]
            image.last_modified_by = images[name]["last_modified_by"]
            image.last_modified_on = images[name]["last_modified_on"]
            image.type = images[name]["type"]
            image.description = images[name]["description"]
            image.docker_url = images[name]["docker_url"]
            image.gpu_docker_url = images[name]["gpu_docker_url"]
            image.category = images[name]["category"]
            session.add(image)
            session.flush()
        else:
            # update data
            for key, val in images[name].items():
                setattr(record, key, val)
            session.add(record)
            session.flush()

    insert_docker(images["Model"]["docker_url"])
    session.commit()


@click.group()
def cli():
    pass


@cli.command()
def create_tables():
    """ create tables in the database """
    db_engine = create_engine("sqlite:////tmp/sqlite.db")
    Base.metadata.create_all(db_engine)


@cli.command()
def create_data():
    """
    create default resource data
    :return:
    """
    create_resource_data()


@cli.command()
def create_image():
    """
    create default docker image data
    :return:
    """
    create_docker_image()






@cli.command()
def keycloak_gatekeeper():
    """ run keycloak gatekeeper """
    executable = shutil.which("keycloak-gatekeeper")
    config_file = config.get("keycloak-gatekeeper", "config_file")
    command = [executable, "--config", config_file]
    subprocess.run(command, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)


@cli.command()
@click.option("--directory", required=True, type=str)
@click.option("--port", type=int, default=8080)
def swagger_ui(directory, port):
    """ run swagger ui """
    os.chdir(directory)
    Handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", port), Handler)
    httpd.serve_forever()


@cli.command()
def gunicorn():
    """ run gunicorn server """
    # run alembic upgrade
    if config.get("run_alembic_script", "upgrade") == "True":
        print("Running alembic upgrade")
        alembicArgs = ["--raiseerr", "upgrade", "head"]
        print("Alembic args: %s", alembicArgs)
        alembic.config.main(argv=alembicArgs)
        alembic_run_status = True
        print("Alembic upgrade is successful")

    # COMMENTED: To Prevent from every restart execution
    # run create resource data
    # create_resource_data()

    # run create docker data
    # create_docker_image()

    # run flask app
    executable = shutil.which("gunicorn")
    config_file = config.get("gunicorn", "config_file")
    command = [executable, "--config", config_file, "mosaic.ai"]
    subprocess.run(command, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)


@cli.command()
def deactivate_model():
    """ Script to stop inactive models """
    from copy import deepcopy
    from sqlalchemy import desc
    from mosaic.ai.models import MLModelDeployment, MLModelRequestLog, MLModel
    from mosaic.ai.constants import DeploymentStatus, Status
    from mosaic.ai import application
    from mosaic_utils.ai.headers.constants import Headers

    deployment_active = [u.__dict__ for u in session.query(MLModelDeployment)
    .filter(MLModelDeployment.deployment_status.in_(
        [DeploymentStatus.Deployed, DeploymentStatus.Failed]))
    .filter(MLModelDeployment.auto_shutdown == Status.active)
    .order_by(desc(MLModelDeployment.created_on))
    .all()]

    deployment = deepcopy(deployment_active)

    model_list = []
    model_to_stop = []
    stopped = []
    failed_to_stop = []
    for model in deployment:
        model_id = model["ml_model_id"]
        model_list.append(model_id)
        try:
            active_logs = (
                session.query(MLModelRequestLog.end_time)
                .filter(MLModelRequestLog.model_id == model_id)
                .order_by(desc(MLModelRequestLog.end_time))
                .first()
            )

            if active_logs is not None and active_logs.end_time > model["last_modified_on"]:
                model_time = active_logs.end_time
            else:
                model_time = model["last_modified_on"]

            time_now = datetime.now()
            total_duration = time_now - model_time
            duration_in_s = total_duration.total_seconds()
            hours = divmod(duration_in_s, 3600)[0]
            max_wait = int(config.get("max_wait_time", "model_time", fallback=2))

            print(model_id, "-hrs -", hours)

            if (hours >= max_wait) and model["deployment_info"] is not None:
                deployment_id = model["id"]
                model_to_stop.append(model_id)

                project = session.query(MLModel.project_id, MLModel.created_by) \
                    .filter(MLModel.id == model_id) \
                    .one()

                client = application.test_client()

                headers = {
                    Headers.x_auth_userid: project.created_by,
                    Headers.x_auth_username: project.created_by,
                    Headers.x_auth_email: project.created_by,
                    Headers.x_project_id: project.project_id,
                    Headers.x_cli_script: project.project_id,
                }

                base_url = config.get("flask", "base_url")

                response = client.delete(
                    f"{base_url}/v1/ml-model/{model_id}/deploy/{deployment_id}",
                    headers=headers,
                )

                if response.status_code == 204:
                    stopped.append(model_id)
                else:
                    failed_to_stop.append({"model_id": model_id, "reason": "Non 204 / keycloak AuthorizationError"})

            if (hours >= max_wait) and model["deployment_info"] is None:
                model_to_stop.append(model_id)
                try:
                    deployment_all = session.query(MLModelDeployment).get(model["id"])
                    session.delete(deployment_all)
                    session.commit()
                    stopped.append(model_id)
                except:
                    failed_to_stop.append({"model_id": model_id, "reason": "DB Delete Failed"})

        except:
            failed_to_stop.append({"model_id": model_id, "reason": "except / project not found"})

    print(len(model_list), "All_models -", model_list)
    print(len(model_to_stop), "Models_to_stop -", model_to_stop)
    print(len(stopped), "Stopped -", stopped)
    print(len(failed_to_stop), "Failed_to_stop -", failed_to_stop)


@cli.command()
def clear_request_logs():
    """ Script to remove models' request logs """
    from datetime import datetime, timedelta
    from mosaic.ai.models import MLModelRequestLog, MLModelVersion
    from mosaic.ai.deployment.manager import delete_request_logs
    from sqlalchemy.exc import SQLAlchemyError
    required_versions = [v for v in session.query(MLModelVersion).all() if
                         v.model_settings is not None and
                         v.model_settings.get("retention_policy_settings") is not None]

    common_path = f'{config.get("MOSAIC-AI-BACKEND-STORAGE", "MOSAIC-AI-BACKEND_MOUNT_PATH")}' + \
                  f'{config.get("MOSAIC-AI-BACKEND-STORAGE", "BUCKET_NAME")}/model-data'
    version_id_list = []
    for version in required_versions:
        retention_policy = version.model_settings.get("retention_policy_settings", {}).get("retention_policy").lower()
        num_days = version.model_settings.get("retention_policy_settings", {}).get("num_days") \
            if retention_policy == "true" else 7
        # Calculate the datetime num_days ago
        num_days_ago = datetime.utcnow() - timedelta(days=num_days)

        # Get the tuples  from the MLModelRequestLog table with request_id as first element and required file path as second element.
        result_tuples = session.query(MLModelRequestLog.request_id,
                                      common_path + '/' + MLModelVersion.ml_model_id + '/' + MLModelVersion.id + '/' +
                                      MLModelRequestLog.request_id + '*') \
            .join(MLModelVersion, MLModelRequestLog.version_id == MLModelVersion.id) \
            .filter(MLModelRequestLog.version_id == version.id) \
            .filter(MLModelRequestLog.end_time <= num_days_ago).all()
        # Extract the request_ids, and nas_paths from the tuples returned by the query and create their list
        request_ids = [t[0] for t in result_tuples]
        file_paths = [t[1] for t in result_tuples]
        if request_ids:
            version_id_list.append(version.id)
            delete_request_logs(file_paths)
            try:
                session.query(MLModelRequestLog) \
                    .filter(MLModelRequestLog.request_id.in_(request_ids)) \
                    .delete(synchronize_session=False)
                session.commit()
            except SQLAlchemyError as e:
                session.rollback()
                print(f"Deletion from the database failed: {e}")
                return str(e)

    if len(version_id_list) > 0:
        print(f'Request logs of these version_ids were deleted from db and NAS storage : {version_id_list}')
    else:
        print('No request logs were deleted')


if __name__ == "__main__":
    cli()
