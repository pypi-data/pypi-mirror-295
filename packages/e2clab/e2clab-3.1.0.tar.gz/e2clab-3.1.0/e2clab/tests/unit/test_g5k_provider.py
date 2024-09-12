"""
Teting e2clab.provider.plugins.G5k module
"""

import enoslib as en
from enoslib import Host, Networks, Roles

import e2clab.constants.default as default
from e2clab.config import InfrastructureConfig
from e2clab.constants import Environment
from e2clab.constants.layers_services import (
    CLUSTER,
    ENV_NAME,
    ENVIRONMENT,
    G5K,
    JOB_NAME,
    JOB_TYPE,
    KEY_NAME,
    LAYERS,
    MONITORING_NETWORK_ROLE,
    MONITORING_SERVICE_ROLE,
    MONITORING_SVC,
    MONITORING_SVC_DSTAT,
    MONITORING_SVC_NETWORK,
    MONITORING_SVC_NETWORK_PRIVATE,
    MONITORING_SVC_NETWORK_SHARED,
    MONITORING_SVC_PORT,
    MONITORING_SVC_PROVIDER,
    MONITORING_SVC_TIG,
    MONITORING_SVC_TPG,
    MONITORING_SVC_TYPE,
    NAME,
    PROVENANCE_SERVICE_ROLE,
    PROVENANCE_SVC,
    PROVENANCE_SVC_DATAFLOW_SPEC,
    PROVENANCE_SVC_PARALLELISM,
    PROVENANCE_SVC_PORT,
    PROVENANCE_SVC_PROVIDER,
    QUANTITY,
    RESERVATION,
    ROLES,
    ROLES_MONITORING,
    SERVERS,
    SERVICES,
    WALLTIME,
)
from e2clab.providers.plugins.G5k import G5k, G5kConfig
from e2clab.tests.unit import TestE2cLab

g5k_config = {
    ENVIRONMENT: {
        JOB_NAME: "test",
        WALLTIME: "01:00:00",
        Environment.G5K.value: {
            JOB_TYPE: ["deploy"],
            CLUSTER: "parasilo",
            ENV_NAME: "debian11-min",
            KEY_NAME: "/home/test/key.pub",
            RESERVATION: "2024-01-01 11:11:11",
        },
    },
    PROVENANCE_SVC: {
        PROVENANCE_SVC_PROVIDER: Environment.G5K.value,
        PROVENANCE_SVC_PARALLELISM: 1,
        CLUSTER: "parasilo",
        PROVENANCE_SVC_DATAFLOW_SPEC: "dataflow-spec.py",
    },
    MONITORING_SVC: {
        MONITORING_SVC_TYPE: MONITORING_SVC_TIG,
        MONITORING_SVC_PROVIDER: Environment.G5K.value,
        CLUSTER: "parasilo",
        MONITORING_SVC_NETWORK: MONITORING_SVC_NETWORK_PRIVATE,
    },
    LAYERS: [
        {
            NAME: "cloud",
            SERVICES: [
                {
                    NAME: "Server",
                    QUANTITY: 1,
                    CLUSTER: "paravance",
                    ROLES: [ROLES_MONITORING],
                }
            ],
        },
        {
            NAME: "fog",
            SERVICES: [
                {
                    NAME: "Gateway",
                    QUANTITY: 1,
                    SERVERS: ["ecotype-1.nantes.grid5000.fr"],
                    ROLES: [ROLES_MONITORING],
                }
            ],
        },
        {
            NAME: "edge",
            SERVICES: [
                {
                    NAME: "Producer",
                    QUANTITY: 1,
                    ENVIRONMENT: Environment.IOT_LAB.value,
                }
            ],
        },
    ],
}
g5k_config_tpg = {
    ENVIRONMENT: {
        JOB_NAME: "test",
        WALLTIME: "01:00:00",
        Environment.G5K.value: {
            JOB_TYPE: ["deploy"],
            CLUSTER: "parasilo",
            ENV_NAME: "debian11-min",
        },
    },
    MONITORING_SVC: {
        MONITORING_SVC_TYPE: MONITORING_SVC_TPG,
        MONITORING_SVC_PROVIDER: Environment.G5K.value,
        CLUSTER: "parasilo",
        MONITORING_SVC_NETWORK: MONITORING_SVC_NETWORK_PRIVATE,
    },
    LAYERS: [
        {
            NAME: "cloud",
            SERVICES: [{NAME: "Server", QUANTITY: 1, CLUSTER: "paravance"}],
        },
        {
            NAME: "fog",
            SERVICES: [
                {
                    NAME: "Gateway",
                    QUANTITY: 1,
                    SERVERS: ["parasilo-14.rennes.grid5000.fr"],
                }
            ],
        },
        {
            NAME: "edge",
            SERVICES: [
                {
                    NAME: "Producer",
                    QUANTITY: 1,
                    ENVIRONMENT: Environment.IOT_LAB.value,
                }
            ],
        },
    ],
}
g5k_config_dstat = {
    ENVIRONMENT: {
        JOB_NAME: "test",
        WALLTIME: "01:00:00",
        Environment.G5K.value: {
            JOB_TYPE: ["deploy"],
            CLUSTER: "parasilo",
            ENV_NAME: "debian11-min",
        },
    },
    MONITORING_SVC: {
        MONITORING_SVC_TYPE: MONITORING_SVC_DSTAT,
    },
    LAYERS: [
        {
            NAME: "cloud",
            SERVICES: [{NAME: "Server", QUANTITY: 1, CLUSTER: "paravance"}],
        },
        {
            NAME: "fog",
            SERVICES: [
                {
                    NAME: "Gateway",
                    QUANTITY: 1,
                    SERVERS: ["parasilo-14.rennes.grid5000.fr"],
                }
            ],
        },
        {
            NAME: "edge",
            SERVICES: [
                {
                    NAME: "Producer",
                    QUANTITY: 1,
                    ENVIRONMENT: Environment.IOT_LAB.value,
                }
            ],
        },
    ],
}
g5k_default_config = {
    ENVIRONMENT: {
        Environment.G5K.value: {CLUSTER: "parasilo", ENV_NAME: "debian11-min"},
    },
    LAYERS: [
        {
            NAME: "cloud",
            SERVICES: [{NAME: "Server", QUANTITY: 1, CLUSTER: "paravance"}],
        },
        {
            NAME: "fog",
            SERVICES: [
                {
                    NAME: "Gateway",
                    QUANTITY: 1,
                    SERVERS: ["parasilo-14.rennes.grid5000.fr"],
                }
            ],
        },
        {
            NAME: "edge",
            SERVICES: [
                {
                    NAME: "Producer",
                    QUANTITY: 1,
                    ENVIRONMENT: Environment.IOT_LAB.value,
                }
            ],
        },
    ],
}


class TestG5kProvider(TestE2cLab):
    """
    Testing G5k provider class
    """

    g5k_infra_config = InfrastructureConfig(g5k_config)
    g5k_infra_config_tpg = InfrastructureConfig(g5k_config_tpg)
    g5k_infra_config_dstat = InfrastructureConfig(g5k_config_dstat)

    def test_G5k(self):
        """Testing a Environment.G5K.value setup"""

        g5k = G5k(infra_config=self.g5k_infra_config, optimization_id=None)

        provider = g5k._provider_g5k()

        prov_conf_dict = provider.provider_conf.to_dict()
        self.assertEqual(prov_conf_dict["job_name"], "test")
        self.assertEqual(prov_conf_dict["walltime"], "01:00:00")
        # 2 services + 1 monitor + 1 provider
        self.assertEqual(len(prov_conf_dict["resources"]["machines"]), 4)

    def test_get_provenance(self):

        g5k = G5k(infra_config=self.g5k_infra_config, optimization_id=None)
        g5k.provenance_provider = False

        provenance_extra_info = g5k.get_provenance()
        self.assertEqual(provenance_extra_info, {})

        g5k.provenance_provider = True

        provenance_extra_info = g5k.get_provenance()
        self.assertEqual(provenance_extra_info, {})

        g5k.roles = Roles({PROVENANCE_SERVICE_ROLE: [Host("1.1.1.1")]})

        provenance_extra_info = g5k.get_provenance()
        self.assertEqual(provenance_extra_info, {})

        g5k.networks = Networks({"test": "dummy"})

        provenance_extra_info = g5k.get_provenance()
        self.assertEqual(
            provenance_extra_info[PROVENANCE_SERVICE_ROLE]["__address__"], "1.1.1.1"
        )
        self.assertEqual(
            provenance_extra_info[PROVENANCE_SERVICE_ROLE]["url"],
            f"http://1.1.1.1:{PROVENANCE_SVC_PORT}",
        )

    def test_get_monitoring(self):

        g5k = G5k(infra_config=self.g5k_infra_config, optimization_id=None)
        g5k.monitoring_provider = False

        monitoring_info = g5k.get_monitoring()
        self.assertEqual(monitoring_info, {})

        g5k.monitoring_provider = True

        monitoring_info = g5k.get_monitoring()
        self.assertEqual(monitoring_info, {})

        g5k.roles = Roles({MONITORING_SERVICE_ROLE: [Host("1.1.1.1")]})

        monitoring_info = g5k.get_monitoring()
        self.assertEqual(monitoring_info, {})

        g5k.networks = Networks({"test": "dummy"})

        monitoring_info = g5k.get_monitoring()
        self.assertEqual(
            monitoring_info[MONITORING_SERVICE_ROLE]["__address__"], "1.1.1.1"
        )
        self.assertEqual(
            monitoring_info[MONITORING_SERVICE_ROLE]["url"],
            f"http://1.1.1.1:{MONITORING_SVC_PORT}",
        )

        g5k = G5k(infra_config=self.g5k_infra_config_tpg, optimization_id=None)
        g5k.monitoring_provider = True
        g5k.roles = Roles({MONITORING_SERVICE_ROLE: [Host("1.1.1.1")]})
        g5k.networks = Networks({"test": "dummy"})

        monitoring_info = g5k.get_monitoring()
        self.assertEqual(
            monitoring_info[MONITORING_SERVICE_ROLE]["__address__"], "1.1.1.1"
        )
        self.assertEqual(
            monitoring_info[MONITORING_SERVICE_ROLE]["url"],
            f"http://1.1.1.1:{MONITORING_SVC_PORT}",
        )

        g5k = G5k(infra_config=self.g5k_infra_config_dstat, optimization_id=None)
        # DSTAT => no monitoring provider
        g5k.monitoring_provider = False
        g5k.roles = Roles({MONITORING_SERVICE_ROLE: [Host("1.1.1.1")]})
        g5k.networks = Networks({"test": "dummy"})

        monitoring_info = g5k.get_monitoring()
        self.assertEqual(monitoring_info, {})


class TestG5kConfig(TestE2cLab):
    """
    Testing G5kConfig class
    """

    def setUp(self) -> None:
        conf = InfrastructureConfig(g5k_config)
        conf.refine_to_environment(Environment.G5K.value)
        self.config = G5kConfig(conf)
        self.config.init(1)

        default_conf = InfrastructureConfig(g5k_default_config)
        default_conf.refine_to_environment(Environment.G5K.value)
        self.default_config = G5kConfig(default_conf)
        self.default_config.init()

    def test_config_init(self):
        self.assertEqual(self.config.job_type, ["deploy"])
        self.assertEqual(self.config.env_name, "debian11-min")
        self.assertEqual(self.config.job_name, "test_1")
        self.assertEqual(self.config.reservation, "2024-01-01 11:11:11")
        self.assertEqual(self.config.walltime, "01:00:00")
        self.assertEqual(self.config.keyfile, "/home/test/key.pub")
        self.assertEqual(self.config.cluster, "parasilo")
        self.assertEqual(set(self.config.cluster_list), {"paravance", "ecotype"})
        self.assertIn("rennes", self.config.prod_network)

    def test_config_default_init(self):
        # Test default parameters parsing
        self.assertEqual(self.default_config.job_type, default.JOB_TYPE)
        self.assertEqual(self.default_config.env_name, "debian11-min")
        self.assertEqual(self.default_config.job_name, default.JOB_NAME)
        self.assertIsNone(self.default_config.reservation)
        self.assertEqual(self.default_config.walltime, default.WALLTIME)
        self.assertEqual(self.default_config.keyfile, default.SSH_KEYFILE)

    def test_config_provenance(self):
        self.config.config_provenance()
        self.assertTrue(self.config.provenance_provider)

        self.default_config.config_provenance()
        self.assertFalse(self.default_config.provenance_provider)

    def test_config_monitoring(self):
        # TODO: complete test
        self.config.config_monitoring()
        self.assertTrue(self.config.monitoring_provider)

        self.default_config.config_monitoring()
        self.assertFalse(self.default_config.monitoring_provider)

    def test_config_resources(self):
        # TODO: Complete test
        self.config.config_provenance()
        self.config.config_monitoring()
        self.config.config_resources()
        self.assertEqual(len(self.config.config.to_dict()["resources"]["machines"]), 4)

    def test_config_finalize(self):
        self.config.config_provenance()
        self.config.config_monitoring()
        self.config.config_resources()
        prov, monitoring, provenance = self.config.finalize()
        self.assertTrue(monitoring)
        self.assertTrue(provenance)
        self.assertIsInstance(prov, en.G5k)

        # Testing with the default configuration
        self.default_config.config_provenance()
        self.default_config.config_monitoring()
        self.default_config.config_resources()
        prov, monitoring, provenance = self.default_config.finalize()
        self.assertFalse(monitoring)
        self.assertFalse(provenance)
        self.assertIsInstance(prov, en.G5k)

    def test_check_monitoring_request(self):
        clusters = self.config._check_monitoring_request()
        self.assertSetEqual(set(clusters), {"ecotype", "paravance"})

    def test_configure_monitoring_helper_funciton(self):
        # Prepare test
        monitoring_config = {
            MONITORING_SVC_TYPE: MONITORING_SVC_TIG,
            MONITORING_SVC_PROVIDER: Environment.G5K.value,
            CLUSTER: "ecotype",
            MONITORING_SVC_NETWORK: MONITORING_SVC_NETWORK_PRIVATE,
        }
        clusters_to_monitor = ["parasilo", "paravance"]
        self.config.monit_private_net = False

        self.config._configure_monitoring(monitoring_config, clusters_to_monitor)

        self.assertTrue(self.config.monit_private_net)
        machines = self.config.config.to_dict()["resources"]["machines"]
        self.assertEqual(len(machines), 1)
        self.assertIn(G5K, machines[0]["roles"])
        self.assertIn(MONITORING_SERVICE_ROLE, machines[0]["roles"])
        self.assertIsNotNone(machines[0]["secondary_networks"])

    def test_configure_monitoring_helper_function_servers(self):
        # Prepare test
        monitoring_config = {
            MONITORING_SVC_TYPE: MONITORING_SVC_TIG,
            MONITORING_SVC_PROVIDER: Environment.G5K.value,
            SERVERS: ["parasilo-1.rennes.grid5000.fr", "ecotype-1.nantes.grid5000.fr"],
            MONITORING_SVC_NETWORK: MONITORING_SVC_NETWORK_SHARED,
        }
        clusters_to_monitor = ["parasilo", "paravance"]
        self.config.monit_private_net = False

        self.config._configure_monitoring(monitoring_config, clusters_to_monitor)

        self.assertFalse(self.config.monit_private_net)
        machines = self.config.config.to_dict()["resources"]["machines"]
        self.assertEqual(len(machines), 1)
        self.assertIn(G5K, machines[0]["roles"])
        self.assertIn(MONITORING_SERVICE_ROLE, machines[0]["roles"])
        self.assertEqual(machines[0]["secondary_networks"], [])
        # Only first server taken into account
        self.assertEqual(machines[0]["servers"], ["parasilo-1.rennes.grid5000.fr"])

    def test_configure_provenance_helper_funciton(self):
        provenance_config = {
            PROVENANCE_SVC_PROVIDER: Environment.G5K.value,
            PROVENANCE_SVC_PARALLELISM: 1,
            CLUSTER: "ecotype",
            PROVENANCE_SVC_DATAFLOW_SPEC: "dataflow-spec.py",
        }
        self.config._configure_provenance(provenance_config)
        machines = self.config.config.to_dict()["resources"]["machines"]
        self.assertEqual(len(machines), 1)
        self.assertIn(G5K, machines[0]["roles"])
        self.assertIn(PROVENANCE_SERVICE_ROLE, machines[0]["roles"])

    def test_configure_provenance_helper_funciton_servers(self):
        provenance_config = {
            PROVENANCE_SVC_PROVIDER: Environment.G5K.value,
            PROVENANCE_SVC_PARALLELISM: 1,
            SERVERS: ["parasilo-1.rennes.grid5000.fr", "ecotype-1.nantes.grid5000.fr"],
            PROVENANCE_SVC_DATAFLOW_SPEC: "dataflow-spec.py",
        }
        self.config._configure_provenance(provenance_config)
        machines = self.config.config.to_dict()["resources"]["machines"]
        self.assertEqual(len(machines), 1)
        self.assertIn(G5K, machines[0]["roles"])
        self.assertIn(PROVENANCE_SERVICE_ROLE, machines[0]["roles"])
        # Only first server taken into account
        self.assertEqual(machines[0]["servers"], ["parasilo-1.rennes.grid5000.fr"])

    def test_get_secondary_network(self):
        self.config.monit_private_net = False
        self.assertIsNone(self.config._get_secondary_networks())

        self.config.monit_private_net = True
        self.config.monit_network = "A"
        self.assertEqual(self.config._get_secondary_networks(), ["A"])

    def test_separate_servers_per_cluster(self):
        servers = [
            "ecotype-1.nantes.grid5000.fr",
            "parasilo-1.rennes.grid5000.fr",
            "ecotype-2.nantes.grid5000.fr",
        ]
        servers_per_cluster = self.config._separate_servers_per_cluster(servers)
        self.assertIn("ecotype", servers_per_cluster)
        self.assertIn("parasilo", servers_per_cluster)
        self.assertEqual(len(servers_per_cluster["ecotype"]), 2)
        self.assertEqual(len(servers_per_cluster["parasilo"]), 1)

    def test_get_sites_from_clusters(self):
        servers = ["ecotype", "parasilo", "paravance"]
        sites = self.config._get_sites_from_clusters(servers)
        self.assertEqual(len(sites), 2)
        self.assertIn("nantes", sites)
        self.assertIn("rennes", sites)

    def test_get_service_clusters(self):
        service_conf = {
            NAME: "test",
            SERVERS: [
                "ecotype-1.nantes.grid5000.fr",
                "parasilo-1.rennes.grid5000.fr",
                "ecotype-2.nantes.grid5000.fr",
            ],
        }
        clusters = self.config._get_service_clusters(service_conf)
        self.assertEqual(len(clusters), 2)
        self.assertIn("ecotype", clusters)
        self.assertIn("parasilo", clusters)

        service_conf = {
            NAME: "test",
        }
        clusters = self.config._get_service_clusters(service_conf)
        self.assertEqual(len(clusters), 1)
        self.assertIn("parasilo", clusters)

    def test_search_clusters_at_service_level(self):
        clusters = self.config._search_clusters_at_service_level()
        self.assertEqual(len(clusters), 2)
        self.assertIn("ecotype", clusters)
        self.assertIn("paravance", clusters)

    def test_create_monitoring_network(self):
        clusters_to_monitor = ["paravance", "parasilo"]
        monitoring_cluster = "paravance"
        net = self.config._create_monitoring_network(
            monitoring_cluster, clusters_to_monitor
        )
        net_conf = net.to_dict()
        self.assertEqual(net_conf["type"], "kavlan")
        self.assertEqual(net_conf["roles"], [MONITORING_NETWORK_ROLE])
        self.assertEqual(net_conf["site"], "rennes")
        self.assertEqual(net_conf["id"], "monitoring_network_rennes")

    def test_create_monitoring_network_global(self):
        clusters_to_monitor = ["ecotype", "parasilo"]
        monitoring_cluster = "paravance"
        net = self.config._create_monitoring_network(
            monitoring_cluster, clusters_to_monitor
        )
        net_conf = net.to_dict()
        self.assertEqual(net_conf["type"], "kavlan-global")
        self.assertEqual(net_conf["roles"], [MONITORING_NETWORK_ROLE])
        self.assertEqual(net_conf["site"], "rennes")
        self.assertEqual(net_conf["id"], "monitoring_network_rennes")

    def test_create_production_network_for_clusters(self):
        clusters = ["ecotype", "parasilo", "paravance"]
        networks = self.config._create_production_network_for_clusters(clusters)

        self.assertIn("nantes", networks)
        self.assertIn("rennes", networks)
