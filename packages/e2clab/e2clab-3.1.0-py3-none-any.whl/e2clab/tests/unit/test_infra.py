"""
Testing e2clab.infra module
"""

import e2clab.infra as e2cinfra
from e2clab.constants import ConfFiles, Environment
from e2clab.constants.layers_services import DEFAULT_SERVICE_NAME
from e2clab.providers.plugins.G5k import G5k
from e2clab.services.plugins.Default import Default
from e2clab.tests.unit import TestE2cLab


class TestInfra(TestE2cLab):
    """
    Testing Infra class
    """

    def setUp(self) -> None:
        self.config = self.test_folder / ConfFiles.LAYERS_SERVICES
        self.infra = e2cinfra.Infrastructure(
            config=self.config,
            optimization_id=None,
        )

    def test_infra_init(self):
        self.assertIsInstance(self.infra, e2cinfra.Infrastructure)
        self.assertIsNone(self.infra.optimization_id)

    def test_infra_prepare(self):
        self.infra.prepare()

        # true if no already imported services
        self.assertEqual(self.infra.prov_to_load, [Environment.G5K.value])
        self.assertIn(DEFAULT_SERVICE_NAME, self.infra.serv_to_load)
        self.assertIn(DEFAULT_SERVICE_NAME, self.infra.available_services)

    def test_load_create_provider(self):
        self.infra.prepare()

        prov = self.infra._load_create_providers()
        self.assertEqual(len(prov), 1)
        self.assertIsInstance(prov[0], G5k)

    def test_load_services(self):
        self.infra.serv_to_load = [DEFAULT_SERVICE_NAME]
        services = self.infra._load_services()

        self.assertEqual(len(services.keys()), 1)
        self.assertEqual(services[DEFAULT_SERVICE_NAME], Default)
