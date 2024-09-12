"""
Testing e2clab.providers.plugins.Chameleonedge module
"""

import enoslib as en

from e2clab.config import InfrastructureConfig
from e2clab.constants import default
from e2clab.constants.layers_services import (
    CHAMELEON_EDGE,
    CLUSTER,
    CONTAINERS,
    ENVIRONMENT,
    IMAGE,
    JOB_NAME,
    LAYERS,
    NAME,
    QUANTITY,
    RC_FILE,
    SERVERS,
    SERVICES,
    WALLTIME,
)
from e2clab.providers.plugins.Chameleonedge import CEConfig, Chameleonedge
from e2clab.tests.unit import TestE2cLab


class TestChameleonEdgeProvider(TestE2cLab):
    """
    Testing Chameleonedge provider class
    """

    def setUp(self):
        chiedge_config_data = {
            ENVIRONMENT: {
                JOB_NAME: "test",
                WALLTIME: "01:00:00",
                CHAMELEON_EDGE: {
                    RC_FILE: "~/rc_file.sh",
                    CLUSTER: "jetson_nano",
                },
            },
            LAYERS: [
                {
                    NAME: "edge",
                    SERVICES: [
                        {
                            NAME: "client",
                            SERVERS: "iot-jetson06",
                            QUANTITY: 4,
                            CONTAINERS: [{NAME: "cli-container", IMAGE: "ubuntu"}],
                        }
                    ],
                }
            ],
        }
        chiedge_config = InfrastructureConfig(chiedge_config_data)

        self.ce = Chameleonedge(infra_config=chiedge_config, optimization_id=None)

    def test_provider(self):
        optimization_id = 10
        provider = self.ce._provider_chameleonedge(optimization_id)

        self.assertIsInstance(provider, en.ChameleonEdge)
        provider_conf = provider.provider_conf.to_dict()

        self.assertEqual(provider_conf["rc_file"], "~/rc_file.sh")
        self.assertEqual(len(provider_conf["resources"]["machines"]), 1)


class TestChameleonEdgeConfig(TestE2cLab):
    """
    Testing CEConfig configuration class
    """

    def setUp(self):
        chiedge_config_data = {
            ENVIRONMENT: {
                JOB_NAME: "test",
                WALLTIME: "01:00:00",
                CHAMELEON_EDGE: {
                    RC_FILE: "~/rc_file.sh",
                    CLUSTER: "jetson_nano",
                },
            },
            LAYERS: [
                {
                    NAME: "edge",
                    SERVICES: [
                        {
                            NAME: "client",
                            CLUSTER: "test",
                            QUANTITY: 4,
                            CONTAINERS: [{NAME: "cli-container", IMAGE: "ubuntu"}],
                        }
                    ],
                }
            ],
        }
        chiedge_config = InfrastructureConfig(chiedge_config_data)
        chiedge_config.refine_to_environment(CHAMELEON_EDGE)
        self.ce_config = CEConfig(chiedge_config)

    def test_init(self):
        self.assertEqual(self.ce_config.job_name, "test")
        self.assertEqual(self.ce_config.walltime, "01:00:00")
        self.assertEqual(self.ce_config.rc_file, "~/rc_file.sh")
        self.assertEqual(self.ce_config.image, default.CHIEDGE_IMAGE)
        self.assertEqual(self.ce_config.cluster, "jetson_nano")

    def test_init_method(self):
        opt_id = 10
        self.ce_config.init(optimization_id=opt_id)

        self.assertEqual(self.ce_config.job_name, f"test_{opt_id}")
        self.assertIsInstance(self.ce_config.config, en.ChameleonEdgeConf)

        self.assertEqual(self.ce_config.config.lease_name, self.ce_config.job_name)
        self.assertEqual(self.ce_config.config.walltime, self.ce_config.walltime)
        self.assertEqual(self.ce_config.config.rc_file, self.ce_config.rc_file)

    def test_config_monitoring(self):
        pass

    def test_config_provenance(self):
        pass

    def test_config_resources(self):
        self.ce_config.init()
        self.ce_config.config_resources()

        config_val = self.ce_config.config.to_dict()
        machines_conf = config_val["resources"]["machines"]
        self.assertEqual(len(machines_conf), 1)
        self.assertEqual(machines_conf[0]["container"]["name"], "cli-container")
        self.assertEqual(machines_conf[0]["count"], 4)
        self.assertEqual(machines_conf[0]["container"]["image"], "ubuntu")

    def test_finalize(self):
        self.ce_config.init()
        prov, is_monitor, is_provenance = self.ce_config.finalize()

        self.assertIsInstance(prov, en.ChameleonEdge)
        self.assertFalse(is_monitor)
        self.assertFalse(is_provenance)
