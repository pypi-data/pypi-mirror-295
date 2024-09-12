from e2clab.config import InfrastructureConfig
from e2clab.constants import ConfFiles, default
from e2clab.constants.layers_services import CLUSTER, ID, NAME, QUANTITY, ROLES, SERVERS
from e2clab.providers import ProviderConfig
from e2clab.tests.unit import TestE2cLab
from e2clab.utils import load_yaml_file


class TestProviderConfig(TestE2cLab):

    def test_init(self):
        layers_conf = load_yaml_file(self.test_folder / ConfFiles.LAYERS_SERVICES)

        conf = ProviderConfig(layers_conf)
        self.assertIsInstance(conf, ProviderConfig)
        self.assertIsInstance(conf, InfrastructureConfig)

        self.assertIsNotNone(conf.env)
        self.assertIsNotNone(conf.layers)

    def test_get_service_quantity(self):

        service_qtty = {NAME: "default", CLUSTER: "parasilo", QUANTITY: 3}
        service = {NAME: "default"}

        self.assertEqual(ProviderConfig.get_service_quantity(service_qtty), 3)
        self.assertEqual(
            ProviderConfig.get_service_quantity(service), default.NODE_QUANTITY
        )

    def test_service_roles(self):

        service1 = {NAME: "default1", ID: "1_1"}
        service2 = {NAME: "default2", ROLES: ["test"], ID: "1_2"}

        roles = ProviderConfig.get_service_roles("cloud", service1)
        self.assertSetEqual(set(roles), set(["cloud", "1_1", "default1"]))

        roles = ProviderConfig.get_service_roles("cloud", service2)
        self.assertSetEqual(set(roles), set(["cloud", "1_2", "default2", "test"]))

    def test_opt_job_id(self):

        self.assertEqual(ProviderConfig.opt_job_id("test", 1), "test_1")

        self.assertEqual(ProviderConfig.opt_job_id("test"), "test")

    def test_check_service_mapping(self):
        service1 = {NAME: "test", CLUSTER: "parasilo"}
        service2 = {NAME: "test", SERVERS: ["test.rennes.grid5000.fr"]}
        service3 = {NAME: "test"}
        service4 = {
            NAME: "test",
            CLUSTER: "parasilo",
            SERVERS: ["test.rennes.grid5000.fr"],
        }

        self.assertEqual(
            ("parasilo", None), ProviderConfig.check_service_mapping(service1)
        )
        self.assertEqual(
            (None, ["test.rennes.grid5000.fr"]),
            ProviderConfig.check_service_mapping(service2),
        )
        self.assertEqual((None, None), ProviderConfig.check_service_mapping(service3))
        self.assertEqual(
            ("parasilo", None), ProviderConfig.check_service_mapping(service4)
        )

    def test_get_clusters_from_servers(self):
        servers = [
            "parasilo-1.rennes.grid5000.fr",
            "parasilo-1.rennes.grid5000.fr",
            "econome-6.nantes.grid5000.fr",
        ]
        clusters = ProviderConfig._get_clusters_from_servers(servers)
        self.assertEqual(len(clusters), 2)
        self.assertEqual(clusters[0], "parasilo")
        self.assertEqual(clusters[1], "econome")
