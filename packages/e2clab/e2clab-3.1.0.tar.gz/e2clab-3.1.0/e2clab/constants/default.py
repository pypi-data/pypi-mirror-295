"""
Default global parameters

Those parameters dictate the default behaviour of experiments

The purpose of this module is to group experiment-level parameters
that are going to be configurable via a config file in the future
"""

from pathlib import Path

from e2clab.constants.layers_services import (
    JOB_TYPE_DEPLOY,
    MONITORING_IOT_AVERAGE_VALS,
    MONITORING_IOT_PERIOD_VALS,
)

# Clusters
G5K_CLUSTER = "paravance"
IOTLAB_CLUSTER = "saclay"
CHAMELEON_CLOUD_CLUSTER = "gpu_rtx_6000"
CHAMELEON_EDGE_CLUSTER = "jetson-nano"
# Experiment
JOB_NAME = "E2Clab"
WALLTIME = "01:00:00"
# Id
SSH_KEYFILE = str(Path.home() / ".ssh" / "id_rsa.pub")
# Services
NODE_QUANTITY = 1
# Providers
G5K_ENV_NAME = "debian11-x64-big"
CHICLOUD_IMAGE = "CC-Ubuntu20.04"
CHIEDGE_IMAGE = "ubuntu"
# Logging
LOG_E2CLAB_PREFIX = "E2C"
LOG_WRITING_MODE = "a+"
LOG_INFO_FILENAME = "e2clab.log"
LOG_ERR_FILENAME = "e2clab.err"
# G5k
JOB_TYPE = [JOB_TYPE_DEPLOY]
# ChameleonEdge
# Default container name
CONTAINER_NAME = "mycontainer"
# Validate files/dir
LAYERS_SERVICES_VALIDATE_FILE = "layers_services-validate.yaml"
NET_VALIDATE_DIR = "network-validate"
WORKFLOW_VALIDATE_FILE = "workflow-validate.out"
# Output folders
PROVENANCE_DATA = "provenance-data"
MONITORING_DATA = "monitoring-data"
MONITORING_IOT_DATA = "iotlab-data"
# Workflow_env
WORKFLOW_ENV_PREFIX = "env_"
# Monitoring IOT
IOT_PERIOD_VAL = MONITORING_IOT_PERIOD_VALS[-1]
IOT_AVERAGE_VAL = MONITORING_IOT_AVERAGE_VALS[1]
