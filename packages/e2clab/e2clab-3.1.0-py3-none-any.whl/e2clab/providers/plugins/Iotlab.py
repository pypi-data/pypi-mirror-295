from typing import Optional, Tuple

import enoslib as en
from enoslib.infra.enos_iotlab.configuration import ConsumptionConfiguration

import e2clab.constants.default as default
from e2clab.config import InfrastructureConfig, ManagerSvcs
from e2clab.constants.layers_services import (
    ARCHI,
    CLUSTER,
    IMAGE,
    IOT_LAB,
    JOB_NAME,
    MONITORING_IOT_AVERAGE,
    MONITORING_IOT_CURRENT,
    MONITORING_IOT_PERIOD,
    MONITORING_IOT_POWER,
    MONITORING_IOT_PROFILES,
    MONITORING_IOT_VOLTAGE,
    NAME,
    PROFILE,
    QUANTITY,
    SERVICES,
    WALLTIME,
)
from e2clab.log import get_logger
from e2clab.providers import Provider, ProviderConfig

logger = get_logger(__name__, ["IOTLAB"])


class Iotlab(Provider):
    """
    The provider to use when deploying on FIT IoT LAB.
    """

    def __init__(self, infra_config: InfrastructureConfig, optimization_id: int):
        super().__init__(infra_config, optimization_id)
        self.infra_config.refine_to_environment(IOT_LAB)
        self.config = IotlabConfig(self.infra_config)

    def init(self):
        """
        Take ownership over some FIT IoT LAB resources (compute and networks).
        :return: roles, networks
        """
        self.provider = self._provider_iotlab(self.optimization_id)

        roles, networks = self.provider.init()
        en.wait_for(roles)

        roles = en.sync_info(roles, networks)

        if None in (roles, networks):
            raise ValueError(f"Failed to get resources from: {IOT_LAB}.")

        self.roles = roles
        self.networks = networks
        self.log_roles_networks(IOT_LAB)

        return roles, networks

    def destroy(self):
        self.provider.destroy()

    # def __provider_iotlab(self, infra_config, optimization_id):
    #     # infra_config.refine_to_environment(IOT_LAB)

    #     logger.info(f" layers_services [{IOT_LAB}] = {self.infra_config}")

    #     # _job_name = infra_config[ENVIRONMENT][JOB_NAME]
    #     #   if JOB_NAME in infra_config[ENVIRONMENT] else default.JOB_NAME
    #     # _walltime = infra_config[ENVIRONMENT][WALLTIME]
    #     #   if WALLTIME in infra_config[ENVIRONMENT] else default.WALLTIME
    #     # _cluster = infra_config[ENVIRONMENT][CLUSTER]
    #     #   if CLUSTER in infra_config[ENVIRONMENT] else default.IOTLAB_CLUSTER

    #     _job_name = infra_config[ENVIRONMENT].get(JOB_NAME, default.JOB_NAME)
    #     _walltime = infra_config[ENVIRONMENT].get(WALLTIME, default.WALLTIME)
    #     _cluster = infra_config[ENVIRONMENT].get(CLUSTER, default.IOTLAB_CLUSTER)

    #     config = en.IotlabConf.from_settings(
    #         job_name=(
    #             f"{_job_name}_{optimization_id}"
    #             if optimization_id is not None
    #             else _job_name
    #         ),
    #         walltime=_walltime,
    #     )

    #     """
    #         MONITORING
    #     """
    #     if MONITORING_IOT_SVC in infra_config:
    #         for profile in infra_config[MONITORING_IOT_SVC][MONITORING_IOT_PROFILES]:
    #             period = profile[MONITORING_IOT_PERIOD]
    #             average = profile[MONITORING_IOT_AVERAGE]
    #             if profile not in MONITORING_IOT_PERIOD_VALS:
    #                 def_period = default.IOT_PERIOD_VAL
    #                 logger.warning(
    #                     "Invalid Iotlab monitor period: "
    #                     f"{period} defaulted to: {def_period}"
    #                 )
    #                 period = def_period
    #             if average not in MONITORING_IOT_AVERAGE_VALS:
    #                 def_average = MONITORING_IOT_AVERAGE_VALS[1]
    #                 logger.warning(
    #                     "Invalid Iotlab monitor average: "
    #                     f"{average} defaulted to: {def_average}"
    #                 )
    #                 average = def_average
    #             config.add_profile(
    #                 name=profile[NAME],
    #                 archi=profile[ARCHI],
    #                 consumption=ConsumptionConfiguration(
    #                     current=(
    #                         True
    #                         if MONITORING_IOT_CURRENT in profile
    #                         and profile[MONITORING_IOT_CURRENT]
    #                         else False
    #                     ),
    #                     power=(
    #                         True
    #                         if MONITORING_IOT_POWER in profile
    #                         and profile[MONITORING_IOT_POWER]
    #                         else False
    #                     ),
    #                     voltage=(
    #                         True
    #                         if MONITORING_IOT_VOLTAGE in profile
    #                         and profile[MONITORING_IOT_VOLTAGE]
    #                         else False
    #                     ),
    #                     period=period,
    #                     average=average,
    #                 ),
    #             )

    #     """
    #         REQUEST RESOURCES
    #     """
    #     for layer in infra_config[LAYERS]:
    #         for service in layer[SERVICES]:
    #             if not self.monitoring_provider:
    #                 self.monitoring_provider = True if "profile" in service else False
    #             add_cluster, add_servers = self.check_service_mapping(service)
    #             if add_cluster is None and add_servers is None:
    #                 add_cluster = _cluster
    #             if add_servers is not None:
    #                 config.add_machine(
    #                     roles=[service[NAME], layer[NAME], service["_id"]]
    #                     + service.get(ROLES, []),
    #                     hostname=add_servers,
    #                     image=service[IMAGE] if IMAGE in service else None,
    #                     profile=service["profile"] if "profile" in service else None,
    #                 )
    #             else:
    #                 config.add_machine(
    #                     roles=[service[NAME], layer[NAME], service["_id"]]
    #                     + service.get(ROLES, []),
    #                     archi=service[ARCHI],
    #                     site=add_cluster,
    #                     number=(
    #                         service[QUANTITY]
    #                         if QUANTITY in service
    #                         else default.NODE_QUANTITY
    #                     ),
    #                     image=service[IMAGE] if IMAGE in service else None,
    #                     profile=service["profile"] if "profile" in service else None,
    #                 )

    #     conf = config.finalize()
    #     logger.debug(f"IOT LAB [conf.to_dict()] = {conf.to_dict()}")
    #     provider = en.Iotlab(conf)
    #     return provider

    def _provider_iotlab(self, optimization_id: Optional[int] = None) -> en.Iotlab:
        self.config.init(optimization_id=optimization_id)
        self.config.config_provenance()
        self.config.config_monitoring()
        self.config.config_resources()
        provider, monitoring_provider, provenance_provider = self.config.finalize()
        self.monitoring_provider = monitoring_provider
        self.provenance_provider = provenance_provider
        return provider


class IotlabConfig(ProviderConfig):
    def __init__(self, data: dict) -> None:
        super().__init__(data)

        self.job_name = self.env.get(JOB_NAME, default.JOB_NAME)
        self.walltime = self.env.get(WALLTIME, default.WALLTIME)
        self.cluster = self.env.get(CLUSTER, default.IOTLAB_CLUSTER)

    def init(self, optimization_id: Optional[int] = None):

        self.job_name = self.opt_job_id(self.job_name, optimization_id)

        self.config = en.IotlabConf.from_settings(
            job_name=self.job_name, walltime=self.walltime
        )

    def config_monitoring(self) -> None:
        """Configure provider config for monitoring"""
        monitoring_conf = self.get_manager_conf(ManagerSvcs.MONITORING_IOT)
        # FIT Iotlab monitoring is not "standard"
        # hence no monitoring provider = True
        if monitoring_conf:
            self._configure_monitoring(monitoring_conf)

    def _configure_monitoring(self, monitoring_conf: dict) -> None:
        for profile in monitoring_conf[MONITORING_IOT_PROFILES]:
            # period and average existance and compliance validated by schema
            period = profile.get(MONITORING_IOT_PERIOD, default.IOT_PERIOD_VAL)
            average = profile.get(MONITORING_IOT_AVERAGE, default.IOT_AVERAGE_VAL)
            current = profile.get(MONITORING_IOT_CURRENT, False)
            power = profile.get(MONITORING_IOT_POWER, False)
            voltage = profile.get(MONITORING_IOT_VOLTAGE, False)
            self.config.add_profile(
                name=profile[NAME],
                archi=profile[ARCHI],
                consumption=ConsumptionConfiguration(
                    current=current,
                    power=power,
                    voltage=voltage,
                    period=period,
                    average=average,
                ),
            )

    def config_provenance(self) -> None:
        pass

    def config_resources(self) -> None:
        for layer in self.layers:
            for service in layer[SERVICES]:
                roles = self.get_service_roles(layer[NAME], service)
                image = service.get(IMAGE, None)
                profile = service.get(PROFILE, None)
                # TODO: Review this
                if not self.monitoring_provider:
                    self.monitoring_provider = True if PROFILE in service else False
                add_cluster, add_servers = self.check_service_mapping(service)
                if add_servers is not None:
                    self.config.add_machine(
                        roles=roles, hostname=add_servers, image=image, profile=profile
                    )
                else:
                    if add_cluster is None:
                        add_cluster = self.cluster
                    archi = service[ARCHI]
                    quantity = service.get(QUANTITY, default.NODE_QUANTITY)
                    self.config.add_machine(
                        roles=roles,
                        archi=archi,
                        site=add_cluster,
                        number=quantity,
                        image=image,
                        profile=profile,
                    )

    def finalize(self) -> Tuple[en.Iotlab, bool, bool]:
        self.config = self.config.finalize()
        logger.debug(f"Provider conf = {self.config.to_dict()}")
        provider = en.Iotlab(self.config)
        return provider, self.monitoring_provider, self.provenance_provider
