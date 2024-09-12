from copy import deepcopy
from typing import Optional, Tuple

import e2clab.constants.default as default
from e2clab.constants import (
    SUPPORTED_ENVIRONMENTS,
    WORKFLOW_TASKS,
    Environment,
    ManagerSvcs,
)
from e2clab.constants.layers_services import (
    DEFAULT_SERVICE_NAME,
    DSTAT_DEFAULT_OPTS,
    DSTAT_OPTIONS,
    ENVIRONMENT,
    ID,
    LAYER_ID,
    LAYER_NAME,
    LAYERS,
    MONITORING_SVC,
    MONITORING_SVC_AGENT_CONF,
    MONITORING_SVC_PROVIDER,
    MONITORING_SVC_TYPE,
    NAME,
    PROVENANCE_SVC,
    PROVENANCE_SVC_DATAFLOW_SPEC,
    PROVENANCE_SVC_PARALLELISM,
    PROVENANCE_SVC_PROVIDER,
    REPEAT,
    SERVICE_ID,
    SERVICE_PLUGIN_NAME,
    SERVICES,
)
from e2clab.constants.network import NETWORKS
from e2clab.constants.workflow import ANSIBLE_TASKS
from e2clab.errors import E2clabConfigError
from e2clab.log import get_logger
from e2clab.schemas import is_valid_conf
from e2clab.services import get_available_services


class E2clabConfig:
    pass


class InfrastructureConfig(dict, E2clabConfig):
    """
    Class to manage infrastructure configuration
    """

    def __init__(self, data: dict, refined: bool = False) -> None:
        """Infrastructure configuration

        Args:
            data (dict): Input data parsed from "layers_services.yaml"
            refined (bool, optional): For producer child classes,
                yielded from "refine_to_environment". Defaults to False.

        Raises:
            E2clabConfigError: Schema error in the input data
        """
        super().__init__(deepcopy(data))
        self.logger = get_logger(__name__, ["INF_CONF"])

        if not refined:
            if not is_valid_conf(self, "layers_services"):
                raise E2clabConfigError
            # pre-process configuration
            self._prepare()

    def _prepare(self):
        """
        Repeats services and generates services ids
        """
        self._repeat_services()
        self._generate_service_id()
        self._set_master_environment()

    def is_provenance_def(self):
        return PROVENANCE_SVC in self.keys()

    def get_provenance_parallelism(self) -> int:
        # No parallelism defined defaults to 1
        parallelism = self[PROVENANCE_SVC].get(PROVENANCE_SVC_PARALLELISM, 1)
        return parallelism

    def get_provenance_dataflow_spec(self):
        dataflow_spec = self[PROVENANCE_SVC].get(PROVENANCE_SVC_DATAFLOW_SPEC, "")
        return dataflow_spec

    def get_monitoring_agent_conf(self) -> str:
        try:
            conf = self[MONITORING_SVC][MONITORING_SVC_AGENT_CONF]
        except KeyError:
            return None
        return conf

    def is_manager_defined(self, manager: ManagerSvcs) -> bool:
        return manager.value in self.keys()

    def get_manager_conf(self, manager: ManagerSvcs) -> Optional[dict]:
        return self.get(manager.value, None)

    def get_monitoring_type(self) -> Optional[str]:
        # If there is Monitoring scv, type is defined per schema
        monitoring_conf = self.get_manager_conf(ManagerSvcs.MONITORING)
        if monitoring_conf:
            # Key presence defined by schema
            return monitoring_conf[MONITORING_SVC_TYPE]
        else:
            return None

    def get_dstat_options(self) -> str:
        try:
            opt = self[MONITORING_SVC][DSTAT_OPTIONS]
        except KeyError:
            self.logger.info(f"DSTAT options defaulting to: {DSTAT_DEFAULT_OPTS}")
            return DSTAT_DEFAULT_OPTS
        return opt

    def get_services_to_load(self) -> Tuple[list[str], list[str]]:
        """Parses configuration to find types of services to load.

        Args:
            infra_config (dict[str, str]): yaml dump of layers_services.yaml
                configuration file

        Returns:
            services_to_load (list[str]): List of types of services
                present in the configuration
            available_services (list[str]): List of currently available Services
        """
        available_services = get_available_services()
        services_to_load = []
        # List services to load
        for layer in self[LAYERS]:
            for service in layer[SERVICES]:
                service_name = service[NAME]
                if service_name not in available_services:
                    # defaults service to 'Default'
                    # TODO: Change implicit behaviour
                    self.logger.info(
                        f"'{service_name}' defaulted to a"
                        f" '{DEFAULT_SERVICE_NAME}' service."
                    )
                    service_name = DEFAULT_SERVICE_NAME
                # Register service plugin name
                service[SERVICE_PLUGIN_NAME] = service_name
                if service_name not in services_to_load:
                    services_to_load.append(service_name)
        return services_to_load, available_services

    def get_providers_to_load(self) -> list[str]:
        """
        Scans for the requested environments.
        :param infra_config: refers to the 'layers_services.yaml' file.
        :return: an array with environment names.
        """
        # Structure of the config is garenteed by the layers-services schema
        prov2load = []
        for environment_key in self[ENVIRONMENT]:
            if environment_key in SUPPORTED_ENVIRONMENTS:
                prov2load.append(environment_key)

        for layer in self[LAYERS]:
            for service in layer[SERVICES]:
                service_env = service.get(ENVIRONMENT)
                if service_env is not None and service_env not in prov2load:
                    self.logger.warning(
                        f"Environment {service[ENVIRONMENT]} "
                        "implicitly defined in layer {layer[NAME]} "
                        "added to requested environments"
                    )
                    prov2load.append(service[ENVIRONMENT])

        self.logger.info(f"Environments to load = {prov2load}")
        return prov2load

    def refine_to_environment(self, target_env: str):
        """Refines the configuration to an environment configuration

        Args:
            target_env (str): environment name
        """
        # Move taget env definition into top level
        if self[ENVIRONMENT].get(target_env):
            self[ENVIRONMENT].update(self[ENVIRONMENT].pop(target_env))

        # Filter other envs definition
        env_defs = list(
            filter(lambda x: x in SUPPORTED_ENVIRONMENTS, self[ENVIRONMENT])
        )
        for env_def in env_defs:
            if env_def != target_env:
                self[ENVIRONMENT].pop(env_def)

        # Filter services
        for layer in reversed(self[LAYERS]):
            for service in reversed(layer[SERVICES]):
                service_env = service.get(ENVIRONMENT, self.master_environment)
                # service_env = service.get(ENVIRONMENT)
                if service_env != target_env:
                    layer[SERVICES].remove(service)

            # Remove empty layers
            if not layer[SERVICES]:
                self[LAYERS].remove(layer)

        # Filtering managers
        for key in ManagerSvcs.value_list():
            if key in self.keys():
                self._filter_manager(ManagerSvcs(key), Environment(target_env))

    # TODO: Move this to a "Manager" class ?
    def _filter_manager(self, manager: ManagerSvcs, target_env: Environment):
        """Removes manager configurations to cater to target environment.

        Args:
            manager (ManagerSvcs): _description_
            target_env (Environment): _description_
        """
        # dict type ensured by schema
        manager_conf: dict = self[manager.value]
        if manager == ManagerSvcs.MONITORING_IOT:
            if target_env != Environment.IOT_LAB:
                self.pop(manager.value)
        elif manager == ManagerSvcs.MONITORING:
            if target_env.value != manager_conf.get(MONITORING_SVC_PROVIDER, None):
                self.pop(manager.value)
        elif manager == ManagerSvcs.PROVENANCE:
            if target_env.value != manager_conf.get(PROVENANCE_SVC_PROVIDER, None):
                self.pop(manager.value)

    def _set_master_environment(self):
        """Save the top-level environment (default for services)"""
        # Master environment is the first one
        envs = filter(lambda x: x in SUPPORTED_ENVIRONMENTS, self[ENVIRONMENT])
        self.master_environment = next(envs)

    def _repeat_services(self):
        """Repeats the Service configuration in the 'layers_services.yaml' file.
        :param infra_config: refers to the 'layers_services.yaml' file.
        """
        for layer in self[LAYERS]:
            for service in layer[SERVICES]:
                if REPEAT in service:
                    for _ in range(service.pop(REPEAT)):
                        layer[SERVICES].append(deepcopy(service))

    def _generate_service_id(self):
        """
        Updates infra_config (layers_services.yaml file defined by users) with
        the _id at the service level.
        An INITIAL (incomplete) Service ID is defined as: "LayerID_ServiceID".
            For example: a Service with ID = "1_1", means first Layer and first
            Service in that layer (as defined in "layers_services.yaml")

        NOTE: The FINAL (complete) "ServiceID" is: "LayerID_ServiceID_MachineID"
            and is generated after Service registration
            (see e2clab.services.Service.__service_key()).
        :param infra_config: refers to the 'layers_services.yaml' file.
        """
        for i, layer in enumerate(self[LAYERS]):
            for j, service in enumerate(layer[SERVICES]):
                layer_id = i + 1
                service_id = j + 1
                service[ID] = str(layer_id) + "_" + str(service_id)
                service[LAYER_NAME] = layer[NAME]
                service[LAYER_ID] = layer_id
                service[SERVICE_ID] = service_id


class NetworkConfig(dict, E2clabConfig):
    """
    Class to manage network configuration
    """

    def __init__(self, data: dict) -> None:
        super().__init__(deepcopy(data))
        if not is_valid_conf(self, "network"):
            raise E2clabConfigError

    def get_networks(self):
        return self.get(NETWORKS, None)


class WorkflowConfig(list, E2clabConfig):
    """
    Class to manage workflow configuration
    """

    def __init__(self, data: list, is_filtered: bool = False) -> None:
        super().__init__(deepcopy(data))
        if not is_valid_conf(self, "workflow"):
            raise E2clabConfigError
        self.is_filtered = is_filtered

    def get_task_filtered_host_config(self, task: str):
        """
            Returns a list of hosts in workflow.yaml (-hosts:)
        with a single task [prepare, launch, finalize] defined in task_filter
        :param task: prepare, or launch, or finalize
        :return: A filtered WorkflowConfig
        """
        if self.is_filtered:
            raise Exception("Cannot filter a Workflow config twice !")
        filtered_host = []
        for host in deepcopy(self):
            if task in host:
                host[ANSIBLE_TASKS] = host.pop(task)
                for other_task in WORKFLOW_TASKS:
                    host.pop(other_task, None)
                filtered_host.append(host)
        return WorkflowConfig(filtered_host, True)


class WorkflowEnvConfig(dict, E2clabConfig):
    """
    Class to manage workflow environment configuration
    """

    def __init__(self, data: dict) -> None:
        super().__init__(deepcopy(data))
        if not is_valid_conf(data, "workflow_env"):
            raise E2clabConfigError
        # TODO: Add a configuration schema validation stage
        self._prefix_env_variables()

    def get_env(self, key: str, default=None) -> None:
        return super(WorkflowEnvConfig, self).get(key, default)

    def _prefix_env_variables(self):
        """Prefixes workflow environment variables"""
        _prefix = default.WORKFLOW_ENV_PREFIX
        for k, v in self.items():
            self[k] = {f"{_prefix}{key}": val for key, val in v.items()}


# TODO: use this object
class ServiceConfig(dict):
    """
    Class to manage Service information
    """

    def __init__(self, data: dict) -> None:
        super().__init__(deepcopy(data))
        pass
