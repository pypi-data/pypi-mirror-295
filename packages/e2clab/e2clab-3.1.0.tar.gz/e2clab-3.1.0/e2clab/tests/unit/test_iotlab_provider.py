"""
Testing e2clab.providers.plugins.Iotlab module
"""

from unittest.mock import MagicMock, patch

import enoslib as en

from e2clab.config import InfrastructureConfig
from e2clab.constants import Environment
from e2clab.constants.layers_services import (
    ARCHI,
    CLUSTER,
    ENVIRONMENT,
    G5K,
    IOT_LAB,
    JOB_NAME,
    LAYERS,
    MONITORING_IOT_AVERAGE,
    MONITORING_IOT_CURRENT,
    MONITORING_IOT_PERIOD,
    MONITORING_IOT_POWER,
    MONITORING_IOT_PROFILES,
    MONITORING_IOT_SVC,
    MONITORING_IOT_VOLTAGE,
    NAME,
    SERVERS,
    SERVICES,
    WALLTIME,
)
from e2clab.providers.plugins.Iotlab import Iotlab, IotlabConfig
from e2clab.tests.unit import TestE2cLab


class TestIotLabPlugin(TestE2cLab):
    """
    Testing Iotlab provider class
    """

    # Can't run config.finalize() on runner
    # No FIT Iotlab credentials foud
    @TestE2cLab.skip_on_runner()
    def test_iot_lab(self):
        """Testing a IotLab setup"""
        iotlab_config = {
            ENVIRONMENT: {
                JOB_NAME: "test",
                WALLTIME: "01:00:00",
                IOT_LAB: {
                    CLUSTER: "grenoble",
                },
            },
            MONITORING_IOT_SVC: {
                MONITORING_IOT_PROFILES: [
                    {
                        NAME: "test_capture",
                        ARCHI: "a8",
                        MONITORING_IOT_PERIOD: 1100,
                        MONITORING_IOT_AVERAGE: 512,
                        MONITORING_IOT_VOLTAGE: True,
                    }
                ]
            },
            LAYERS: [
                {
                    NAME: "cloud",
                    SERVICES: [{NAME: "Server", ENVIRONMENT: G5K}],
                },
                {NAME: "edge", SERVICES: [{NAME: "Producer", ARCHI: "a8:at86rf231"}]},
            ],
        }

        iotlab_config = InfrastructureConfig(iotlab_config)

        iotlab = Iotlab(infra_config=iotlab_config, optimization_id=None)

        self.assertIsInstance(iotlab, Iotlab)
        provider = iotlab._provider_iotlab()

        prov_conf_dict = provider.provider_conf.to_dict()
        self.assertEqual(prov_conf_dict["job_name"], "test")
        self.assertTrue(
            prov_conf_dict["monitoring"]["profiles"][0]["consumption"][
                MONITORING_IOT_VOLTAGE
            ]
        )
        self.assertFalse(
            prov_conf_dict["monitoring"]["profiles"][0]["consumption"][
                MONITORING_IOT_CURRENT
            ]
        )
        self.assertFalse(
            prov_conf_dict["monitoring"]["profiles"][0]["consumption"][
                MONITORING_IOT_POWER
            ]
        )
        self.assertEqual(prov_conf_dict["walltime"], "01:00:00")
        self.assertEqual(len(prov_conf_dict["resources"]["machines"]), 1)


class TestIotLabConfig(TestE2cLab):
    """
    Testing IotlabConfig class
    """

    def setUp(self):
        iotlab_config = {
            ENVIRONMENT: {
                JOB_NAME: "test",
                WALLTIME: "01:00:30",
                IOT_LAB: {
                    CLUSTER: "grenoble",
                },
            },
            MONITORING_IOT_SVC: {
                MONITORING_IOT_PROFILES: [
                    {
                        NAME: "test_capture",
                        ARCHI: "a8",
                        MONITORING_IOT_PERIOD: 1100,
                        MONITORING_IOT_AVERAGE: 512,
                        MONITORING_IOT_VOLTAGE: True,
                    }
                ]
            },
            LAYERS: [
                {
                    NAME: "cloud",
                    SERVICES: [{NAME: "Server", ENVIRONMENT: G5K}],
                },
                {NAME: "edge", SERVICES: [{NAME: "Producer", ARCHI: "a8:at86rf231"}]},
                {
                    NAME: "edge2",
                    SERVICES: [
                        {
                            NAME: "Producer",
                            SERVERS: [
                                "a8-1.grenoble.iot-lab.info",
                                "a8-2.grenoble.iot-lab.info",
                            ],
                        }
                    ],
                },
            ],
        }
        infra_conf = InfrastructureConfig(iotlab_config)
        infra_conf.refine_to_environment(Environment.IOT_LAB.value)
        self.conf = IotlabConfig(infra_conf)

    def test_init(self):

        self.assertEqual(self.conf.job_name, "test")
        self.assertEqual(self.conf.walltime, "01:00:30")
        self.assertEqual(self.conf.cluster, "grenoble")

    def test_init_method(self):

        self.conf.init(1)
        self.assertEqual(self.conf.job_name, "test_1")
        self.assertIsInstance(self.conf.config, en.IotlabConf)

    def test_config_monitoring(self):

        self.conf.init()
        with patch.object(IotlabConfig, "_configure_monitoring") as m_config_monitoring:

            self.conf.config_monitoring()
            m_config_monitoring.assert_called_once()

    def test_configure_monitoring_helper_function(self):

        monitoring_config = {
            MONITORING_IOT_PROFILES: [
                {
                    NAME: "test_capture",
                    ARCHI: "a8",
                    MONITORING_IOT_PERIOD: 1100,
                    MONITORING_IOT_AVERAGE: 512,
                    MONITORING_IOT_VOLTAGE: True,
                }
            ]
        }
        self.conf.init()
        self.conf._configure_monitoring(monitoring_config)
        profiles = self.conf.config.to_dict()["monitoring"]["profiles"]
        self.assertEqual(len(profiles), 1)
        self.assertEqual(profiles[0]["archi"], "a8")
        self.assertEqual(profiles[0]["name"], "test_capture")
        self.assertTrue(profiles[0]["consumption"]["voltage"])
        self.assertFalse(profiles[0]["consumption"]["current"])
        self.assertFalse(profiles[0]["consumption"]["power"])
        self.assertEqual(profiles[0]["consumption"]["average"], 512)
        self.assertEqual(profiles[0]["consumption"]["period"], 1100)

    def test_configure_provenance(self):
        self.conf.init()
        before = self.conf.config.to_dict()
        self.conf.config_provenance()

        # Function does nothing
        self.assertDictEqual(before, self.conf.config.to_dict())

    def test_config_resources(self):
        # TODO: Improve testing
        self.conf.init()
        self.conf.config_resources()
        data = self.conf.config.to_dict()

        self.assertEqual(len(data["resources"]["machines"]), 2)
        self.assertEqual(data["resources"]["machines"][0]["archi"], "a8:at86rf231")
        self.assertEqual(len(data["resources"]["machines"][1]["hostname"]), 2)

    # TODO: fix patching to avoid initializing an iotlab client on a runner
    @TestE2cLab.skip_on_runner()
    @patch("enoslib.IotlabConf.finalize")
    def test_finalize(self, p_finalize: MagicMock):
        self.conf.init()
        prov, monitoring_provider, provenance_provider = self.conf.finalize()

        p_finalize.assert_called_once()
        self.assertIsInstance(prov, en.Iotlab)
        self.assertFalse(monitoring_provider)
        self.assertFalse(provenance_provider)
