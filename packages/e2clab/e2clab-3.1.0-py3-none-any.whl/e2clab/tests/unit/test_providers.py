"""
Testing e2clab.providers.provider module
"""

import e2clab.providers as e2cprov
from e2clab.config import InfrastructureConfig
from e2clab.constants import SUPPORTED_ENVIRONMENTS, ConfFiles
from e2clab.providers.errors import E2clabProviderImportError
from e2clab.tests.unit import TestE2cLab
from e2clab.utils import load_yaml_file


# TODO: improve testing by checking default configurations
class TestProvidersUtils(TestE2cLab):
    """
    Testing Provider base class methods
    """

    def test_get_available_providers(self):
        available_providers = e2cprov.get_available_providers()
        for prov in SUPPORTED_ENVIRONMENTS:
            self.assertIn(prov.capitalize(), available_providers)

    def test_load_providers(self):
        providers_to_load = [prov.capitalize() for prov in SUPPORTED_ENVIRONMENTS]
        loaded_providers = e2cprov.load_providers(providers_to_load)

        self.assertEqual(set(providers_to_load), set(loaded_providers.keys()))

        data = load_yaml_file(self.test_folder / ConfFiles.LAYERS_SERVICES)
        config = InfrastructureConfig(data)

        for prov in providers_to_load:
            provider_inst = loaded_providers[prov](
                infra_config=config, optimization_id=None
            )
            self.assertIsInstance(provider_inst, e2cprov.Provider)

        with self.assertRaises(E2clabProviderImportError):
            e2cprov.load_providers(["notaprovider"])
