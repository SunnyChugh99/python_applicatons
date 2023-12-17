# -*- coding: utf-8 -*-
"""mosaic ai tables module"""
from datetime import datetime

import sqlalchemy as sa
from flask import g
from sqlalchemy.dialects import mysql
from sqlalchemy.ext.declarative import declarative_base
from mosaic_utils.ai.encoding_utils import fix_padding
from .constants import DeploymentStatus, DockerImageType, InputType, \
    ModelFlavours, DockerImageCategory, Status
from .utils import (
    get_db_type,
    get_default_docker_image_url,
    get_default_gpu_docker_image_url,
    get_default_resource_id,
    uuid_generator,
    get_docker_url_for_kyd
)
from .constants import ResourceStatus

Base = declarative_base()
# pylint: disable=invalid-name, too-few-public-methods
db_type = get_db_type()


class ModelMixin:
    """Base table for mosaic ai"""
    id = sa.Column(sa.String(100), primary_key=True, default=uuid_generator)
    created_by = sa.Column(sa.String(100), default=lambda: g.userid)
    created_on = sa.Column(sa.DateTime, default=datetime.utcnow)
    last_modified_by = sa.Column(sa.String(100), default=lambda: g.userid)
    last_modified_on = sa.Column(
        sa.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            if getattr(self, key):
                setattr(self, key, val)


class MLModelResource(Base):
    """Model for ML model resources"""
    __tablename__ = "ml_model_resource"
    id = sa.Column(sa.String(100), primary_key=True, default=uuid_generator)
    name = sa.Column(sa.String(100))
    cpu_request = sa.Column(sa.String(20))
    ram_request = sa.Column(sa.String(20))
    cpu_limit = sa.Column(sa.String(20))
    ram_limit = sa.Column(sa.String(20))
    gpu = sa.Column(sa.String(20), default="")
    min_replicas = sa.Column(sa.String(20), default="1")
    max_replicas = sa.Column(sa.String(20), default="1")
    gpu_type = sa.Column(sa.String(20), default="")
    status = sa.Column(
        sa.Enum(
            ResourceStatus.ENABLED,
            ResourceStatus.DISABLED
        ),
        default=ResourceStatus.ENABLED
    )

    # backref
    ml_models = sa.orm.relationship("MLModel", back_populates="resource")
    deployments = sa.orm.relationship("MLModelDeployment", back_populates="resource")


class MLModel(Base, ModelMixin):
    """Model for ML model"""
    __tablename__ = "ml_models"

    name = sa.Column(sa.String(100))
    description = sa.Column(sa.String(500))
    flavour = sa.Column(sa.String(20), default=ModelFlavours.application)
    tags = sa.Column(sa.JSON)
    project_id = sa.Column(sa.String(100), default=lambda: g.project_id)

    resource_id = sa.Column(
        sa.String(100),
        sa.ForeignKey("ml_model_resource.id"),
        default=get_default_resource_id,
    )
    status = sa.Column(sa.String(10), default="active")
    type = sa.Column(sa.String(30))
    model_display = sa.Column(sa.Boolean, default=True)
    source = sa.Column(sa.String(10), default="")

    # backref
    versions = sa.orm.relationship("MLModelVersion", back_populates="ml_model")
    deployments = sa.orm.relationship("MLModelDeployment", back_populates="ml_model")
    resource = sa.orm.relationship("MLModelResource", back_populates="ml_models")


class MLModelVersion(Base, ModelMixin):
    """Model for ML model version"""
    __tablename__ = "ml_model_versions"

    object_url = sa.Column(sa.String(200))
    ml_model_id = sa.Column(sa.String(100), sa.ForeignKey("ml_models.id"), index=True)
    ml_model_id = sa.Column(sa.String(100), sa.ForeignKey("ml_models.id"), index=True)
    description = sa.Column(sa.String(500))
    schema = sa.Column(sa.JSON)
    metadata_info = sa.Column(sa.JSON)
    deploy_info = sa.Column(sa.JSON)
    status = sa.Column(sa.String(10), default="active")
    init_script = sa.Column(sa.Text, default="")
    docker_image_url = sa.Column(sa.String(300), default=get_default_docker_image_url)
    gpu_docker_image_url = sa.Column(sa.String(300), default=get_default_gpu_docker_image_url)
    input_type = sa.Column(sa.Enum(InputType.json, InputType.file))
    target_names = sa.Column(sa.JSON)
    datasource_name = sa.Column(sa.String(200))
    model_class = sa.Column(sa.JSON)
    model_info = sa.Column(sa.JSON)
    version_no = sa.Column(sa.Integer)
    dependent_model = sa.Column(sa.JSON)
    repo_details = sa.Column(sa.JSON)
    nas_details = sa.Column(sa.JSON)
    model_settings = sa.Column(sa.JSON)

    stage = sa.Column(sa.String(200))

    # backref
    ml_model = sa.orm.relationship("MLModel", back_populates="versions")
    deployments = sa.orm.relationship("MLModelDeployment", back_populates="version")
    metrics = sa.orm.relationship("MLModelMetrics", back_populates="versions")
    profiling = sa.orm.relationship("MLModelProfiling", back_populates="versions")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.init_script:
            self.init_script = fix_padding(self.init_script)


class MLModelDeployment(Base, ModelMixin):
    """Model for ML model deployment"""
    __tablename__ = "ml_model_deployments"

    name = sa.Column(sa.String(100))
    ml_model_id = sa.Column(sa.String(100), sa.ForeignKey("ml_models.id"), index=True)
    version_id = sa.Column(sa.String(100), sa.ForeignKey("ml_model_versions.id"))
    resource_id = sa.Column(sa.String(100), sa.ForeignKey("ml_model_resource.id"))
    deployment_info = sa.Column(sa.JSON)
    deployment_status = sa.Column(
        sa.Enum(DeploymentStatus.Deploying, DeploymentStatus.Deployed, DeploymentStatus.Failed)
    )

    # backrefs
    ml_model = sa.orm.relationship("MLModel", back_populates="deployments")
    version = sa.orm.relationship("MLModelVersion", back_populates="deployments")
    resource = sa.orm.relationship("MLModelResource", back_populates="deployments")
    auto_shutdown = sa.Column(sa.String(10), nullable=False, default=Status.active)


class UserTokens(Base, ModelMixin):
    """Model for User tokens"""
    __tablename__ = "ml_model_tokens"
    username = sa.Column(sa.String(100))
    jwt = sa.Column(sa.String(500))


class MLModelRequestLog(Base):
    """Model for ML model request log"""
    __tablename__ = "ml_model_request_log"
    request_id = sa.Column(
        sa.String(100), primary_key=True, nullable=False, default=uuid_generator
    )
    model_id = sa.Column(sa.String(100), nullable=False)
    version_id = sa.Column(sa.String(100), nullable=False)
    if db_type == "mysql":
        start_time = sa.Column(mysql.DATETIME(fsp=6))
        end_time = sa.Column(mysql.DATETIME(fsp=6))
    else:
        start_time = sa.Column(sa.DateTime)
        end_time = sa.Column(sa.DateTime)
    status = sa.Column(sa.String(100))
    feedback = sa.Column(sa.String(20))
    metric_value = sa.Column(sa.JSON)


class MLModelProfiling(Base, ModelMixin):
    """Model for ML model profiling"""
    __tablename__ = "ml_model_profiling"
    ml_model_id = sa.Column(sa.String(100), sa.ForeignKey("ml_models.id"), index=True)
    version_id = sa.Column(sa.String(100), sa.ForeignKey("ml_model_versions.id"))
    column_name = sa.Column(sa.String(100))
    datasource_name = sa.Column(sa.String(100))
    profiling = sa.Column(sa.JSON)

    # backref
    versions = sa.orm.relationship("MLModelVersion", back_populates="profiling")


class MLModelMetrics(Base, ModelMixin):
    """Model for ML model metrics"""
    __tablename__ = "ml_model_metrics"
    metric_value = sa.Column(sa.LargeBinary(length=(2 ** 32) - 1))
    pipeline_id = sa.Column(sa.String(100), index=True)
    ml_model_id = sa.Column(sa.String(100), sa.ForeignKey("ml_models.id"), index=True)
    version_id = sa.Column(
        sa.String(100), sa.ForeignKey("ml_model_versions.id"), index=True
    )
    tag = sa.Column(sa.String(100))
    annotation = sa.Column(sa.String(500))
    nlg = sa.Column(sa.Text)

    # backref
    versions = sa.orm.relationship("MLModelVersion", back_populates="metrics")


class MLDockerImage(Base, ModelMixin):
    """ Model for docker image """

    __tablename__ = "ml_docker_image"
    type = sa.Column(sa.Enum(DockerImageType.PRE_BUILD, DockerImageType.CUSTOM_BUILD))
    name = sa.Column(sa.String(200), nullable=False)
    description = sa.Column(sa.String(200))
    docker_url = sa.Column(sa.String(200), nullable=False)
    gpu_docker_url = sa.Column(sa.String(200), nullable=False)
    category = sa.Column(sa.Enum(DockerImageCategory.MODEL, DockerImageCategory.APPLICATION))


class MLKYDDataStore(Base, ModelMixin):
    """ Model for KYD Data Store """

    __tablename__ = "ml_kyd_data_store"

    ml_model_id = sa.Column(sa.String(100), sa.ForeignKey("ml_models.id"), index=True)
    version_id = sa.Column(sa.String(100), sa.ForeignKey("ml_model_versions.id"))

    data_type = sa.Column(sa.String(20))
    inference_type = sa.Column(sa.String(20))
    feature_name = sa.Column(sa.String(100))
    truth_values = sa.Column(sa.String(200))

    distribution_actual = sa.Column(sa.JSON)
    distribution_predicted = sa.Column(sa.JSON)

    run_at = sa.Column(sa.DateTime)

    __table_args__ = (
        sa.UniqueConstraint('ml_model_id',
                            'version_id',
                            'data_type',
                            'inference_type',
                            'feature_name',
                            'truth_values',
                            name='_kyd_records_uc'),
    )

    def __repr__(self):
        return '{}: ML({}/{}) Current Selection: {} -> {}'.format(self.id,
                                                                  self.ml_model_id,
                                                                  self.version_id,
                                                                  self.feature_name,
                                                                  self.truth_values)


class MLKYDDriftScore(Base, ModelMixin):
    """ Model for KYD Drift Score """

    __tablename__ = "ml_kyd_drift_score"

    ml_model_id = sa.Column(sa.String(100), sa.ForeignKey("ml_models.id"), index=True)
    version_id = sa.Column(sa.String(100), sa.ForeignKey("ml_model_versions.id"))
    algorithm = sa.Column(sa.String(100))
    algorithm_input = sa.Column(sa.JSON)
    score_output = sa.Column(sa.JSON)
    run_at = sa.Column(sa.DateTime)

    def __repr__(self):
        return '{}: ML({}/{}) Drift Score: {}'.format(self.id,
                                                      self.ml_model_id,
                                                      self.version_id,
                                                      self.score_output)


class MLKydJobSettings(Base, ModelMixin):
    """ Model for MLKydJobSettings """

    __tablename__ = "ml_kyd_job_settings"

    ml_model_id = sa.Column(sa.String(100), sa.ForeignKey("ml_models.id"), index=True)
    version_id = sa.Column(sa.String(100), sa.ForeignKey("ml_model_versions.id"))
    baseline_data = sa.Column(sa.String(300), default="train_data")
    baseline_config = sa.Column(sa.JSON, nullable=True)
    data_to_use = sa.Column(sa.String(100))
    dto_use_config = sa.Column(sa.JSON, nullable=True)
    data_stats = sa.Column(sa.Boolean, default=True)
    image_to_use = sa.Column(sa.String(300), default=get_docker_url_for_kyd)
    job_frequency = sa.Column(sa.String(100))
    ds_algorithm = sa.Column(sa.String(200), default="ks")
    ds_config = sa.Column(sa.JSON, nullable=True)
    feat_at_risk = sa.Column(sa.String(10), nullable=True)
    feat_at_fail = sa.Column(sa.String(10), nullable=True)
    job_prefix = sa.Column(sa.String(100), default="kyd-")
    job_name = sa.Column(sa.String(200), nullable=True)
    is_cron = sa.Column(sa.Boolean, nullable=True)
    container_name = sa.Column(sa.String(100), default="kyd-checkpoint")
    cpu = sa.Column(sa.String(10), default="2")
    memory = sa.Column(sa.String(10), default="2Gi")
    past_weeks = sa.Column(sa.String(10), default="4")
    extra_config = sa.Column(sa.JSON, nullable=True)
    outlier_algo = sa.Column(sa.String(40), default="iqr")
    outlier_threshold = sa.Column(sa.String(10), default="3")
    outlier_lower_quantile = sa.Column(sa.String(10), default="0.1")
    outlier_upper_quantile = sa.Column(sa.String(10), default="0.9")

    def __repr__(self):
        return '{}: ML({}/{}) Job Settings: {}-{}'.format(self.id,
                                                          self.ml_model_id,
                                                          self.version_id,
                                                          self.data_to_use,
                                                          self.job_frequency)


class MLKydJobRunHistory(Base, ModelMixin):
    """ Model for MLKydJobRunHistory """

    __tablename__ = "ml_kyd_job_run_history"

    ml_model_id = sa.Column(sa.String(100), sa.ForeignKey("ml_models.id"), index=True)
    version_id = sa.Column(sa.String(100), sa.ForeignKey("ml_model_versions.id"))
    run_at = sa.Column(sa.DateTime, default=datetime.utcnow)

    job_name = sa.Column(sa.String(200), nullable=True)
    is_cron = sa.Column(sa.Boolean, nullable=True)
    pod_name = sa.Column(sa.String(200), nullable=True)
    snapshot_name = sa.Column(sa.String(300), nullable=True)
    init = sa.Column(sa.Boolean, nullable=True)
    running = sa.Column(sa.Boolean, nullable=True)
    completed = sa.Column(sa.Boolean, nullable=True)

    message = sa.Column(sa.Text)

    def __repr__(self):
        return '{}: ML({}/{}) KydJobRunHistory: {}-{}'.format(self.id,
                                                              self.ml_model_id,
                                                              self.version_id,
                                                              self.data_type,
                                                              self.run_at)


class MLKydStatistics(Base, ModelMixin):
    """ Model for MLKydStatistics """

    __tablename__ = "ml_kyd_stats"

    ml_model_id = sa.Column(sa.String(100), sa.ForeignKey("ml_models.id"), index=True)
    version_id = sa.Column(sa.String(100), sa.ForeignKey("ml_model_versions.id"))
    run_at = sa.Column(sa.DateTime, default=datetime.utcnow)

    data_name = sa.Column(sa.String(200))
    feature_name = sa.Column(sa.String(300))
    property = sa.Column(sa.String(300))
    property_value = sa.Column(sa.String(300), nullable=True)
    property_json = sa.Column(sa.JSON, nullable=True)

    def __repr__(self):
        return '{}: ML({}/{}) MLKydStatistics: {}-{}'.format(self.id,
                                                             self.ml_model_id,
                                                             self.version_id,
                                                             self.data_name,
                                                             self.run_at)


class MLKydPredictionOverTime(Base, ModelMixin):
    """ Model for MLKydPredictionOverTime """

    __tablename__ = "ml_kyd_prediction_over_time"

    ml_model_id = sa.Column(sa.String(100), sa.ForeignKey("ml_models.id"), index=True)
    version_id = sa.Column(sa.String(100), sa.ForeignKey("ml_model_versions.id"))
    run_at = sa.Column(sa.DateTime, default=datetime.utcnow)

    model_type = sa.Column(sa.String(200), nullable=True)
    data_name = sa.Column(sa.String(200), nullable=False)
    mean = sa.Column(sa.Float, nullable=True)
    lower_percentile = sa.Column(sa.Float, nullable=True)
    upper_percentile = sa.Column(sa.Float, nullable=True)
    count = sa.Column(sa.BigInteger, nullable=True)
    outliers = sa.Column(sa.BigInteger, default=0)
    percentage = sa.Column(sa.JSON, nullable=True)

    def __repr__(self):
        return '{}: ML({}/{}) PredictionOverTime: {}-{}'.format(self.id,
                                                                self.ml_model_id,
                                                                self.version_id,
                                                                self.data_name,
                                                                self.run_at)
