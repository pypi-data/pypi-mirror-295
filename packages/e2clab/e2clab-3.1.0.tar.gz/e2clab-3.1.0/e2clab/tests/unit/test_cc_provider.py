"""
Testing e2clab.providers.plugin.Chameleoncloud module
"""

from unittest.mock import patch

from enoslib import CBM, CBMConf

from e2clab.config import InfrastructureConfig
from e2clab.constants.layers_services import (
    CHAMELEON_CLOUD,
    CLUSTER,
    ENVIRONMENT,
    IMAGE,
    JOB_NAME,
    KEY_NAME,
    LAYERS,
    MONITORING_SERVICE_ROLE,
    MONITORING_SVC,
    MONITORING_SVC_PROVIDER,
    MONITORING_SVC_TIG,
    MONITORING_SVC_TYPE,
    NAME,
    RC_FILE,
    ROLES,
    SERVICES,
    WALLTIME,
)
from e2clab.providers.plugins.Chameleoncloud import CCConfig, Chameleoncloud
from e2clab.tests.unit import TestE2cLab


class TestChameleonCloudPlugin(TestE2cLab):
    """
    Testing ChameleonCloud provider class
    """

    def setUp(self):
        chameleoncloud_config = {
            ENVIRONMENT: {
                JOB_NAME: "test",
                WALLTIME: "01:00:00",
                CHAMELEON_CLOUD: {
                    RC_FILE: "~/rc_file.sh",
                    IMAGE: "CC-Ubuntu20.04",
                    KEY_NAME: "id_rsa.pub",
                    CLUSTER: "compute_skylake",
                },
            },
            MONITORING_SVC: {
                MONITORING_SVC_TYPE: MONITORING_SVC_TIG,
                MONITORING_SVC_PROVIDER: CHAMELEON_CLOUD,
                CLUSTER: "compute_skylake",
            },
            LAYERS: [
                {NAME: "cloud", SERVICES: [{NAME: "server", ROLES: ["monitoring"]}]}
            ],
        }
        chameleoncloud_config = InfrastructureConfig(chameleoncloud_config)

        self.cc = Chameleoncloud(
            infra_config=chameleoncloud_config, optimization_id=None
        )

    def test_provider(self):
        """Testing a Chameleon Cloud setup"""

        self.assertIsInstance(self.cc, Chameleoncloud)
        # self.chameleon_cloud.init(testing=True)
        provider = self.cc._provider_chameleoncloud()
        self.assertIsInstance(provider, CBM)

        prov_conf_dict = provider.provider_conf.to_dict()

        # What is happening here ?
        # self.assertEqual(prov_conf_dict["lease_name"], "test")
        # self.assertEqual(prov_conf_dict["walltime"], "01:00:00")
        self.assertEqual(prov_conf_dict["rc_file"], "~/rc_file.sh")

        # 1 more machine for monitoring
        self.assertEqual(len(prov_conf_dict["resources"]["machines"]), 2)

        self.assertTrue(self.cc.monitoring_provider)
        self.assertFalse(self.cc.provenance_provider)


class TestChameleonCloudConfig(TestE2cLab):
    """
    Testing CCConfig configuration class
    """

    def setUp(self):
        self.chicloud_monitoring_config = {
            ENVIRONMENT: {
                JOB_NAME: "test",
                WALLTIME: "01:00:00",
                CHAMELEON_CLOUD: {
                    RC_FILE: "~/rc_file.sh",
                    IMAGE: "CC-Ubuntu20.04",
                    KEY_NAME: "id_rsa.pub",
                    CLUSTER: "compute_skylake",
                },
            },
            MONITORING_SVC: {
                MONITORING_SVC_TYPE: MONITORING_SVC_TIG,
                MONITORING_SVC_PROVIDER: CHAMELEON_CLOUD,
                CLUSTER: "compute_skylake",
            },
            LAYERS: [
                {NAME: "cloud", SERVICES: [{NAME: "server", ROLES: ["monitoring"]}]}
            ],
        }
        monitoring_infra_config = InfrastructureConfig(self.chicloud_monitoring_config)
        monitoring_infra_config.refine_to_environment(CHAMELEON_CLOUD)
        self.cc_monitor_config = CCConfig(monitoring_infra_config)
        self.cc_monitor_config.init()

        self.chicloud_config = {
            ENVIRONMENT: {
                JOB_NAME: "test",
                WALLTIME: "01:00:00",
                CHAMELEON_CLOUD: {
                    RC_FILE: "~/rc_file.sh",
                    IMAGE: "CC-Ubuntu20.04",
                    KEY_NAME: "id_rsa.pub",
                    CLUSTER: "compute_skylake",
                },
            },
            LAYERS: [
                {NAME: "cloud", SERVICES: [{NAME: "server", ROLES: ["monitoring"]}]}
            ],
        }
        infra_config = InfrastructureConfig(self.chicloud_config)
        infra_config.refine_to_environment(CHAMELEON_CLOUD)
        self.cc_config = CCConfig(infra_config)
        self.cc_config.init()

    def test_init(self):
        self.assertEqual(self.cc_monitor_config.job_name, "test")
        self.assertEqual(self.cc_monitor_config.walltime, "01:00:00")
        self.assertEqual(self.cc_monitor_config.rc_file, "~/rc_file.sh")
        self.assertEqual(self.cc_monitor_config.key_name, "id_rsa.pub")
        self.assertEqual(self.cc_monitor_config.image, "CC-Ubuntu20.04")
        self.assertEqual(self.cc_monitor_config.cluster, "compute_skylake")

    def test_init_method(self):
        opt_id = 10
        self.cc_monitor_config.init(optimization_id=opt_id)

        self.assertEqual(self.cc_monitor_config.job_name, f"test_{opt_id}")
        self.assertIsInstance(self.cc_monitor_config.config, CBMConf)

        self.assertEqual(
            self.cc_monitor_config.config.lease_name, self.cc_monitor_config.job_name
        )
        self.assertEqual(
            self.cc_monitor_config.config.walltime, self.cc_monitor_config.walltime
        )
        self.assertEqual(
            self.cc_monitor_config.config.rc_file, self.cc_monitor_config.rc_file
        )
        self.assertEqual(
            self.cc_monitor_config.config.key_name, self.cc_monitor_config.key_name
        )
        self.assertEqual(
            self.cc_monitor_config.config.image, self.cc_monitor_config.image
        )

    def test_configure_monitoring(self):
        monitoring_config = self.chicloud_monitoring_config.get(MONITORING_SVC)
        self.cc_monitor_config._configure_monitoring(monitoring_config)

        data = self.cc_monitor_config.config.to_dict()
        self.assertEqual(len(data["resources"]["machines"]), 1)
        self.assertEqual(
            data["resources"]["machines"][0]["roles"], [MONITORING_SERVICE_ROLE]
        )

    def test_config_monitoring(self):
        self.cc_monitor_config.config_monitoring()

        self.assertTrue(self.cc_monitor_config.monitoring_provider)
        data = self.cc_monitor_config.config.to_dict()
        self.assertEqual(len(data["resources"]["machines"]), 1)
        self.assertEqual(
            data["resources"]["machines"][0]["roles"], [MONITORING_SERVICE_ROLE]
        )

        self.cc_config.config_monitoring()
        self.assertFalse(self.cc_config.monitoring_provider)
        data = self.cc_config.config.to_dict()
        self.assertEqual(len(data["resources"]["machines"]), 0)

    @patch("enoslib.CBM")
    def test_finalize(self, mock_cbm):
        _, monitoring_provider, provenance_provider = self.cc_monitor_config.finalize()
        mock_cbm.assert_called_once_with(self.cc_monitor_config.config)

        self.assertFalse(monitoring_provider)
        self.assertFalse(provenance_provider)
