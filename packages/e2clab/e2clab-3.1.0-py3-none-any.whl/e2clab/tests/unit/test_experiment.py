"""
Testing e2clab.experiment module
"""

import shutil
from pathlib import Path
from unittest.mock import MagicMock, call, patch

from enoslib import Networks, Roles

from e2clab.constants import default
from e2clab.errors import E2clabError
from e2clab.experiment import Experiment
from e2clab.infra import Infrastructure
from e2clab.network import Network
from e2clab.tests.unit import TestE2cLab


class TestExperiment(TestE2cLab):
    """
    Testing Experiment class
    """

    def setUp(self) -> None:
        # Default experiment
        self.def_exp = Experiment(
            scenario_dir=self.test_folder,
            artifacts_dir=self.test_folder,
        )

    def tearDown(self) -> None:
        # Removing output folder
        shutil.rmtree(self.def_exp.experiment_dir, True)

    def test_init(self):
        self.assertIsNone(self.def_exp.repeat)
        self.assertIsNone(self.def_exp.optimization_config)
        self.assertIsNone(self.def_exp.optimization_id)
        self.assertEqual(self.def_exp.app_conf_list, [])

        self.assertIsInstance(self.def_exp.id, str)

    def test_initiate(self):

        with self.assertLogs("e2clab.experiment", level="INFO") as _:
            self.def_exp.initiate()

        self.assertTrue(Path(self.def_exp.experiment_dir).exists())
        self.assertTrue(
            Path(self.def_exp.experiment_dir / default.LOG_INFO_FILENAME).exists()
        )
        self.assertTrue(
            Path(self.def_exp.experiment_dir / default.LOG_ERR_FILENAME).exists()
        )

    @patch.object(Experiment, "_dump_application_parameters")
    @patch("e2clab.experiment.Infrastructure", autospec=True)
    def test_infrastructure(self, MockInfra: MagicMock, MockDump: MagicMock):
        infra = MockInfra.return_value
        infra.deploy.return_value = (Roles({}), Networks({}))

        self.def_exp.initiate()
        self.def_exp.infrastructure()

        infra.deploy.assert_called_once_with(
            artifacts_dir=self.test_folder,
            remote_working_dir=self.def_exp.monitoring_remote_working_dir,
        )
        infra.deploy.assert_called_once()
        MockDump.assert_called_once()
        self.assertIsInstance(self.def_exp.infra, Infrastructure)

    def test_network_no_infra(self):
        self.def_exp.initiate()
        with self.assertRaises(E2clabError):
            self.def_exp.network()

    @patch("e2clab.experiment.Network", autospec=True)
    def test_network(self, MockNetwork: MagicMock):
        # Prepare test
        self.def_exp.initiate()
        self.def_exp.infra = True
        self.def_exp.roles = Roles({})
        self.def_exp.networks = Networks({})

        net = MockNetwork.return_value

        self.def_exp.network()
        net.prepare.assert_called_once()
        net.deploy.assert_called_once()
        net.validate.assert_called_once()
        self.assertIsInstance(self.def_exp.net, Network)

    def test_application_no_infra(self):
        self.def_exp.initiate()
        with self.assertRaises(E2clabError):
            self.def_exp.application("prepare")

    @patch("e2clab.experiment.Infrastructure")
    @patch("e2clab.experiment.App", autospec=True)
    def test_application(self, MockApp: MagicMock, MockInfra: MagicMock):
        app = MockApp.return_value
        infra = MockInfra.return_value
        infra.all_serv_extra_inf.return_value = {}

        self.def_exp.initiate()
        self.def_exp.infra = infra
        self.def_exp.roles = Roles({})
        self.def_exp.networks = Networks({})

        self.def_exp.application("prepare")

        app.run_task.assert_called_once_with(task="prepare", current_repeat=None)

    def test_finalize_no_infra(self):
        self.def_exp.initiate()
        with self.assertRaises(E2clabError):
            self.def_exp.finalize()

    @patch("e2clab.experiment.Infrastructure", autospec=True)
    @patch("e2clab.experiment.App", autospec=True)
    def test_finalize(self, MockApp: MagicMock, MockInfra: MagicMock):
        app = MockApp.return_value
        infra = MockInfra.return_value

        self.def_exp.initiate()
        self.def_exp.infra = infra
        self.def_exp.app = app
        self.def_exp.roles = Roles({})
        self.def_exp.networks = Networks({})

        self.def_exp.finalize()

        app.run_task.assert_called_once_with("finalize", current_repeat=None)
        infra.finalize.assert_called_once_with(output_dir=self.def_exp.experiment_dir)

    @patch("e2clab.experiment.Infrastructure", autospec=True)
    @patch("e2clab.experiment.App", autospec=True)
    def test_finalize_app_dir(self, MockApp: MagicMock, MockInfra: MagicMock):
        app = MockApp.return_value
        infra = MockInfra.return_value

        self.def_exp.initiate()
        self.def_exp.infra = infra
        self.def_exp.app = app
        self.def_exp.roles = Roles({})
        self.def_exp.networks = Networks({})

        self.def_exp.finalize(app_conf="test")

        app.run_task.assert_called_once_with("finalize", current_repeat=None)
        output_dir = self.def_exp.experiment_dir / "test"
        infra.finalize.assert_called_once_with(output_dir=output_dir)

    @patch.object(Experiment, "initiate")
    @patch.object(Experiment, "infrastructure")
    @patch.object(Experiment, "network")
    @patch.object(Experiment, "_run_deploy")
    def test_deploy(self, mock_run_deploy, mock_network, mock_infra, mock_initiate):
        self.def_exp.deploy(duration=10)

        mock_run_deploy.assert_called_once_with(10, True, None)
        mock_network.assert_called_once()
        mock_infra.assert_called_once()
        mock_initiate.assert_called_once()

    @patch.object(Experiment, "initiate")
    @patch.object(Experiment, "infrastructure")
    @patch.object(Experiment, "network")
    @patch.object(Experiment, "_run_deploy", autospec=True)
    def test_deploy_app_conf(
        self,
        mock_run_deploy: MagicMock,
        mock_network: MagicMock,
        mock_infra: MagicMock,
        mock_initiate: MagicMock,
    ):
        self.def_exp.app_conf_list = ["test", "opt"]
        mock_run_deploy.return_value = False
        self.def_exp.deploy(duration=10)

        mock_run_deploy.assert_called_with(self.def_exp, 10, False, "opt")
        mock_network.assert_called_once()
        mock_infra.assert_called_once()
        mock_initiate.assert_called_once()

    @patch.object(Experiment, "application")
    @patch.object(Experiment, "finalize")
    def test_run_deploy(self, mock_finalize: MagicMock, mock_application: MagicMock):
        is_prepare = self.def_exp._run_deploy(0, True, None)

        self.assertFalse(is_prepare)

        calls = [call("prepare"), call("launch", None)]

        mock_application.assert_has_calls(calls)
        mock_finalize.assert_called_once_with(app_conf=None)

    @patch("e2clab.experiment.Infrastructure", autospec=True)
    def test_destroy(self, MockInfra: MagicMock):
        infra = MockInfra.return_value

        self.def_exp.infra = infra
        self.def_exp.destroy()
        infra.destroy.assert_called_once()
