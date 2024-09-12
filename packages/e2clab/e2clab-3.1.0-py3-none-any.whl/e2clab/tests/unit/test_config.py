import e2clab.config as e2cconf
from e2clab.constants import Environment, ManagerSvcs
from e2clab.constants.layers_services import (
    ARCHI,
    CLUSTER,
    DEFAULT_SERVICE_NAME,
    DSTAT_DEFAULT_OPTS,
    DSTAT_OPTIONS,
    ENVIRONMENT,
    ID,
    JOB_NAME,
    LAYER_ID,
    LAYER_NAME,
    LAYERS,
    MONITORING_IOT_AVERAGE,
    MONITORING_IOT_PERIOD,
    MONITORING_IOT_PROFILES,
    MONITORING_IOT_SVC,
    MONITORING_SVC,
    MONITORING_SVC_AGENT_CONF,
    MONITORING_SVC_DSTAT,
    MONITORING_SVC_PROVIDER,
    MONITORING_SVC_TIG,
    MONITORING_SVC_TYPE,
    NAME,
    PROVENANCE_SVC,
    PROVENANCE_SVC_DATAFLOW_SPEC,
    PROVENANCE_SVC_PROVIDER,
    REPEAT,
    SERVICE_ID,
    SERVICE_PLUGIN_NAME,
    SERVICES,
    WALLTIME,
)
from e2clab.constants.network import NETWORKS
from e2clab.constants.workflow import (
    ANSIBLE_TASKS,
    DEPENDS_ON,
    TARGET,
    TASK_FINALIZE,
    TASK_LAUNCH,
    TASK_PREPARE,
)
from e2clab.errors import E2clabConfigError
from e2clab.tests.unit import TestE2cLab


class TestInfraConfig(TestE2cLab):

    def setUp(self):

        self.df_spec = "dataflow_spec_file"

        self.valid_conf = {
            ENVIRONMENT: {
                JOB_NAME: "test",
                WALLTIME: "01:00:00",
                Environment.G5K.value: {CLUSTER: "parasilo"},
            },
            LAYERS: [
                {NAME: "cloud", SERVICES: [{NAME: "Exp", REPEAT: 3}]},
                {NAME: "edge", SERVICES: [{NAME: "Prod", REPEAT: 1}]},
            ],
            PROVENANCE_SVC: {
                PROVENANCE_SVC_PROVIDER: Environment.G5K.value,
                CLUSTER: "parasilo",
                PROVENANCE_SVC_DATAFLOW_SPEC: self.df_spec,
            },
            MONITORING_SVC: {MONITORING_SVC_TYPE: MONITORING_SVC_DSTAT},
        }

        self.valid_conf2 = {
            ENVIRONMENT: {
                JOB_NAME: "test",
                WALLTIME: "01:00:00",
                Environment.G5K.value: {CLUSTER: "parasilo"},
            },
            LAYERS: [
                {NAME: "cloud", SERVICES: [{NAME: "Exp", REPEAT: 3}]},
                {NAME: "edge", SERVICES: [{NAME: "Prod", REPEAT: 1}]},
            ],
            PROVENANCE_SVC: {
                PROVENANCE_SVC_PROVIDER: Environment.G5K.value,
                CLUSTER: "parasilo",
                PROVENANCE_SVC_DATAFLOW_SPEC: self.df_spec,
            },
            MONITORING_SVC: {
                MONITORING_SVC_TYPE: MONITORING_SVC_TIG,
                DSTAT_OPTIONS: "-m -c",
                MONITORING_SVC_AGENT_CONF: "conf",
            },
        }

        self.multiprov_valid_conf = {
            ENVIRONMENT: {
                JOB_NAME: "test",
                WALLTIME: "01:00:00",
                Environment.G5K.value: {CLUSTER: "parasilo"},
                Environment.IOT_LAB.value: {CLUSTER: "grenoble"},
            },
            LAYERS: [
                {
                    NAME: "cloud",
                    SERVICES: [
                        {NAME: "Exp", ENVIRONMENT: Environment.G5K.value, REPEAT: 3},
                        {NAME: "Serv"},
                    ],
                },
                {
                    NAME: "fog",
                    SERVICES: [
                        {
                            NAME: "Fog",
                            ENVIRONMENT: Environment.CHAMELEON_CLOUD.value,
                            REPEAT: 3,
                        }
                    ],
                },
                {
                    NAME: "edge",
                    SERVICES: [
                        {
                            NAME: "Prod",
                            ENVIRONMENT: Environment.IOT_LAB.value,
                            REPEAT: 1,
                        }
                    ],
                },
            ],
            PROVENANCE_SVC: {
                PROVENANCE_SVC_PROVIDER: Environment.G5K.value,
                CLUSTER: "parasilo",
                PROVENANCE_SVC_DATAFLOW_SPEC: self.df_spec,
            },
            MONITORING_SVC: {
                MONITORING_SVC_TYPE: MONITORING_SVC_TIG,
                MONITORING_SVC_PROVIDER: Environment.G5K.value,
            },
            MONITORING_IOT_SVC: {
                MONITORING_IOT_PROFILES: [
                    {
                        NAME: "Test",
                        ARCHI: "a8",
                        MONITORING_IOT_AVERAGE: 1024,
                        MONITORING_IOT_PERIOD: 8244,
                    }
                ]
            },
        }

    def test_config_prepare(self):
        with self.assertRaises(E2clabConfigError):
            not_a_conf = {"not_a_key": []}
            e2cconf.InfrastructureConfig(not_a_conf)

        conf = e2cconf.InfrastructureConfig(self.valid_conf)
        self.assertIsInstance(conf, dict)
        # Testing prepare method
        self.assertEqual(len(conf[LAYERS][0][SERVICES]), 4)
        self.assertEqual(len(conf[LAYERS][1][SERVICES]), 2)
        self.assertEqual(conf[LAYERS][0][SERVICES][1][ID], "1_2")
        self.assertEqual(conf[LAYERS][1][SERVICES][0][ID], "2_1")
        self.assertEqual(conf[LAYERS][0][SERVICES][1][LAYER_ID], 1)
        self.assertEqual(conf[LAYERS][1][SERVICES][0][LAYER_ID], 2)
        self.assertEqual(conf[LAYERS][0][SERVICES][1][SERVICE_ID], 2)
        self.assertEqual(conf[LAYERS][1][SERVICES][0][SERVICE_ID], 1)
        self.assertEqual(conf[LAYERS][0][SERVICES][1][LAYER_NAME], "cloud")
        self.assertEqual(conf[LAYERS][1][SERVICES][0][LAYER_NAME], "edge")

    def test_config_default(self):
        conf = e2cconf.InfrastructureConfig(self.valid_conf)
        self.assertIsInstance(conf, dict)

        # Testing default options
        self.assertTrue(conf.is_provenance_def())
        self.assertAlmostEqual(conf.get_provenance_parallelism(), 1)
        self.assertEqual(conf.get_dstat_options(), DSTAT_DEFAULT_OPTS)
        self.assertIsNone(conf.get_monitoring_agent_conf())

        conf2 = e2cconf.InfrastructureConfig(self.valid_conf2)
        self.assertEqual(conf2.get_provenance_dataflow_spec(), self.df_spec)
        self.assertEqual(conf2.get_monitoring_agent_conf(), "conf")
        self.assertEqual(conf2.get_dstat_options(), "-m -c")

    def test_services_to_load(self):
        conf = e2cconf.InfrastructureConfig(self.valid_conf)
        self.assertIsInstance(conf, dict)

        services_to_load, available_services = conf.get_services_to_load()
        self.assertEqual(services_to_load, [DEFAULT_SERVICE_NAME])
        self.assertIn(DEFAULT_SERVICE_NAME, available_services)
        # Check that the service name has been added to the configuration
        for layer in conf[LAYERS]:
            for service in layer[SERVICES]:
                self.assertIn(SERVICE_PLUGIN_NAME, service.keys())

    def test_providers_to_load(self):
        conf = e2cconf.InfrastructureConfig(self.valid_conf)
        self.assertIsInstance(conf, dict)

        providers_to_load = conf.get_providers_to_load()
        self.assertIn(Environment.G5K.value, providers_to_load)

        conf2 = e2cconf.InfrastructureConfig(self.multiprov_valid_conf)

        providers_to_load = conf2.get_providers_to_load()
        self.assertIn(Environment.G5K.value, providers_to_load)
        self.assertIn(Environment.IOT_LAB.value, providers_to_load)
        self.assertIn(Environment.CHAMELEON_CLOUD.value, providers_to_load)
        self.assertNotIn(Environment.CHAMELEON_EDGE.value, providers_to_load)

        # Test that you must at least have an environment in ENVIRONMENT
        multiprov_invalid_conf = {
            ENVIRONMENT: {
                JOB_NAME: "test",
                WALLTIME: "01:00:00",
            },
            LAYERS: [
                {
                    NAME: "cloud",
                    SERVICES: [
                        {NAME: "Exp", ENVIRONMENT: Environment.G5K.value, REPEAT: 3}
                    ],
                },
                {
                    NAME: "edge",
                    SERVICES: [
                        {
                            NAME: "Prod",
                            ENVIRONMENT: Environment.IOT_LAB.value,
                            REPEAT: 1,
                        }
                    ],
                },
            ],
        }
        with self.assertRaises(E2clabConfigError):
            conf2 = e2cconf.InfrastructureConfig(multiprov_invalid_conf)

    def test_set_master_environment(self):
        conf = e2cconf.InfrastructureConfig(self.multiprov_valid_conf)
        self.assertEqual(conf.master_environment, Environment.G5K.value)

    def test_refine_to_environment(self):
        conf = e2cconf.InfrastructureConfig(self.multiprov_valid_conf)
        conf.refine_to_environment(Environment.IOT_LAB.value)

        self.assertNotIn(Environment.G5K.value, conf[ENVIRONMENT])
        self.assertNotIn(Environment.IOT_LAB.value, conf[ENVIRONMENT])
        self.assertEqual(conf[ENVIRONMENT][CLUSTER], "grenoble")

        self.assertEqual(len(conf[LAYERS]), 1)
        self.assertEqual(conf[LAYERS][0][NAME], "edge")
        self.assertEqual(len(conf[LAYERS][0][SERVICES]), 2)

        conf = e2cconf.InfrastructureConfig(self.multiprov_valid_conf)
        conf.refine_to_environment(Environment.G5K.value)

        self.assertNotIn(Environment.G5K.value, conf[ENVIRONMENT])
        self.assertNotIn(Environment.IOT_LAB.value, conf[ENVIRONMENT])
        self.assertEqual(conf[ENVIRONMENT][CLUSTER], "parasilo")

        self.assertEqual(len(conf[LAYERS]), 1)
        self.assertEqual(conf[LAYERS][0][NAME], "cloud")
        self.assertEqual(len(conf[LAYERS][0][SERVICES]), 5)

        conf = e2cconf.InfrastructureConfig(self.multiprov_valid_conf)
        conf.refine_to_environment(Environment.CHAMELEON_CLOUD.value)

        self.assertNotIn(Environment.G5K.value, conf[ENVIRONMENT])
        self.assertNotIn(Environment.IOT_LAB.value, conf[ENVIRONMENT])
        self.assertNotIn(CLUSTER, conf[ENVIRONMENT])

        self.assertEqual(len(conf[LAYERS]), 1)
        self.assertEqual(conf[LAYERS][0][NAME], "fog")
        self.assertEqual(len(conf[LAYERS][0][SERVICES]), 4)

    def test_filter_manager(self):
        # Testing _filter_manager
        conf = e2cconf.InfrastructureConfig(self.multiprov_valid_conf)
        conf.refine_to_environment(Environment.G5K.value)

        self.assertNotIn(MONITORING_IOT_SVC, conf)
        self.assertIn(MONITORING_SVC, conf)
        self.assertIn(PROVENANCE_SVC, conf)

        conf = e2cconf.InfrastructureConfig(self.multiprov_valid_conf)
        conf.refine_to_environment(Environment.CHAMELEON_CLOUD.value)

        self.assertNotIn(MONITORING_IOT_SVC, conf)
        self.assertNotIn(MONITORING_SVC, conf)
        self.assertNotIn(PROVENANCE_SVC, conf)

        conf = e2cconf.InfrastructureConfig(self.multiprov_valid_conf)
        conf.refine_to_environment(Environment.IOT_LAB.value)

        self.assertIn(MONITORING_IOT_SVC, conf)
        self.assertNotIn(MONITORING_SVC, conf)
        self.assertNotIn(PROVENANCE_SVC, conf)

    def test_get_manager_conf(self):
        conf = e2cconf.InfrastructureConfig(self.multiprov_valid_conf)

        for manager_type in ManagerSvcs:
            manager_conf = conf.get_manager_conf(manager_type)
            self.assertIsNotNone(manager_conf)

        conf = e2cconf.InfrastructureConfig(self.valid_conf2)
        self.assertIsNone(conf.get_manager_conf(ManagerSvcs.MONITORING_IOT))

    def test_is_manager_defined(self):
        conf = e2cconf.InfrastructureConfig(self.multiprov_valid_conf)

        for manager_type in ManagerSvcs:
            manager_conf = conf.is_manager_defined(manager_type)
            self.assertTrue(manager_conf)

        conf = e2cconf.InfrastructureConfig(self.valid_conf2)
        self.assertFalse(conf.is_manager_defined(ManagerSvcs.MONITORING_IOT))


class TestNetworkConfig(TestE2cLab):

    def test_network_config(self):
        with self.assertRaises(E2clabConfigError):
            not_a_conf = {"notanetwork": []}
            e2cconf.NetworkConfig(not_a_conf)

        valid_conf = {NETWORKS: None}
        conf = e2cconf.NetworkConfig(valid_conf)
        self.assertIsInstance(conf, dict)


class TestWorkflowConfig(TestE2cLab):

    def test_workflow_config(self):
        with self.assertRaises(E2clabConfigError):
            not_a_conf = [{"notaworkflow": 0}]
            e2cconf.WorkflowConfig(not_a_conf)

        workflow_conf = [
            {
                TARGET: "cloud",
                DEPENDS_ON: [],
                TASK_PREPARE: [{"debug": {"msg": "test prepare"}}],
                TASK_LAUNCH: [{"debug": {"msg": "test launch"}}],
                TASK_FINALIZE: [{"debug": {"msg": "test finalize"}}],
            },
            {
                TARGET: "fog",
                DEPENDS_ON: [],
                TASK_PREPARE: [{"debug": {"msg": "test prepare"}}],
                TASK_FINALIZE: [{"debug": {"msg": "test finalize"}}],
            },
            {
                TARGET: "edge",
                DEPENDS_ON: [],
                TASK_PREPARE: [{"debug": {"msg": "test prepare"}}],
                TASK_LAUNCH: [{"debug": {"msg": "test launch"}}],
                TASK_FINALIZE: [{"debug": {"msg": "test finalize"}}],
            },
        ]

        conf = e2cconf.WorkflowConfig(workflow_conf)
        prepare_filtered = conf.get_task_filtered_host_config(TASK_PREPARE)
        launch_filtered = conf.get_task_filtered_host_config(TASK_LAUNCH)

        self.assertEqual(len(prepare_filtered), 3)
        self.assertEqual(len(launch_filtered), 2)
        self.assertIn(ANSIBLE_TASKS, prepare_filtered[0])
        self.assertIn(ANSIBLE_TASKS, launch_filtered[0])

        # Test can't filter a conf twice
        with self.assertRaises(Exception):
            launch_filtered.get_task_filtered_host_config(TASK_FINALIZE)

    def test_workflow_env_config(self):
        invalid_conf = {"base": {"A": {"B": 4}}}
        valid_conf = {
            "base": {"A": 5, "B": "hello"},
            "custom": {"A": 5, "B": "hello", "C": 4.2},
        }
        conf = e2cconf.WorkflowEnvConfig(valid_conf)
        with self.assertRaises(E2clabConfigError):
            e2cconf.WorkflowEnvConfig(invalid_conf)

        base_env = conf.get_env("base")
        no_env = conf.get_env("not_a_conf", {})

        self.assertEqual(no_env, {})
        self.assertEqual(base_env, {"env_A": 5, "env_B": "hello"})
