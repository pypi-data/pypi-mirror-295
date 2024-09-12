"""
Testing CLI interface
"""

import os
import shutil
from pathlib import Path
from unittest.mock import MagicMock, patch

from click.testing import CliRunner

import e2clab.cli as e2cli
from e2clab.constants import PATH_SERVICES_PLUGINS, Command, ConfFiles
from e2clab.tests.unit import TestE2cLab


class TestCLI(TestE2cLab):
    """
    Testing CLI interface
    """

    def setUp(self):

        self.test_service = self.test_folder / "service" / "Default2.py"
        self.test_notaservice = self.test_folder / "service" / "Default3.py"

        self.runner = CliRunner()
        self.invalid_test_folder = self.test_folder / "tmp"
        os.mkdir(self.invalid_test_folder)
        for file in self.test_folder.glob("invalid_*"):
            dest_name = file.name.replace("invalid_", "")
            dest_path = self.invalid_test_folder / dest_name
            shutil.copy(file, dest_path)

    def tearDown(self):
        shutil.rmtree(self.invalid_test_folder)

    @patch("enoslib.check")
    def test_check_testbeds(self, p_check: MagicMock):
        result = self.runner.invoke(e2cli.check_testbeds, [])
        self.assertEqual(result.exit_code, 0)
        p_check.assert_called_once()

    def test_check_argument(self):
        folder = str(self.test_folder)
        invalid_folder = str(self.invalid_test_folder)
        result = self.runner.invoke(e2cli.check_configuration, [folder])
        self.assertEqual(result.exit_code, 0)
        result = self.runner.invoke(e2cli.check_configuration, [folder, "-c", "deploy"])
        self.assertEqual(result.exit_code, 0)
        result = self.runner.invoke(
            e2cli.check_configuration, [folder, "-c", "notacommand"]
        )
        self.assertEqual(result.exit_code, 2)
        result = self.runner.invoke(e2cli.check_configuration, [invalid_folder])
        self.assertEqual(result.exit_code, 1)
        result = self.runner.invoke(e2cli.check_configuration, ["Notafolder"])
        self.assertEqual(result.exit_code, 2)

    def test_services_list(self):
        result = self.runner.invoke(e2cli.list, [])
        self.assertEqual(result.exit_code, 0)

    def test_services_add(self):
        result = self.runner.invoke(e2cli.add, ["dontexist"])
        self.assertEqual(result.exit_code, 2)

        is_a_folder = self.test_folder
        folder_path = self.get_filepath_str(is_a_folder)
        result = self.runner.invoke(e2cli.add, [folder_path])
        self.assertEqual(result.exit_code, 1)

        not_python_file = self.test_folder / ConfFiles.WORKFLOW
        file_path = self.get_filepath_str(not_python_file)
        result = self.runner.invoke(e2cli.add, [file_path])
        self.assertEqual(result.exit_code, 1)

        dummy_service = self.test_service
        dummy_file_path = self.get_filepath_str(dummy_service)

        # Try adding a service using a copy
        result = self.runner.invoke(e2cli.add, [dummy_file_path, "--copy"])
        self.assertEqual(result.exit_code, 0)

        # Try adding an already present service
        result = self.runner.invoke(e2cli.add, [dummy_file_path])
        self.assertEqual(result.exit_code, 1)

        file_to_clean = PATH_SERVICES_PLUGINS / dummy_service.name
        file_to_clean.unlink()

        # Try adding a serice using a symlink
        result = self.runner.invoke(e2cli.add, [dummy_file_path, "--link"])
        self.assertEqual(result.exit_code, 0)

        file_to_clean = PATH_SERVICES_PLUGINS / dummy_service.name
        file_to_clean.unlink()

        # Try importing an invalid service
        inv_service = self.get_filepath_str(self.test_notaservice)
        result = self.runner.invoke(e2cli.add, [inv_service])
        self.assertEqual(result.exit_code, 1)

    def test_services_remove(self):
        result = self.runner.invoke(e2cli.remove, ["Default"])
        self.assertEqual(result.exit_code, 1)

        result = self.runner.invoke(e2cli.remove, ["Notaservice"])
        self.assertEqual(result.exit_code, 1)

        # Copying a valid dummy service to be removed
        shutil.copy(self.test_service, PATH_SERVICES_PLUGINS)

        result = self.runner.invoke(e2cli.remove, [self.test_service.stem])
        self.assertEqual(result.exit_code, 0)

    def test_parse_comma_list(self):
        app_conf = "abc,xyz,123"
        parsed_list = e2cli.parse_comma_list(None, None, app_conf)

        self.assertEqual(parsed_list, ["abc", "xyz", "123"])

    @patch("e2clab.tasks.deploy")
    def test_deploy_notapath(self, _):
        result = self.runner.invoke(e2cli.deploy, ["notapath", "notapath"])
        self.assertEqual(result.exit_code, 2)

    @patch("e2clab.tasks.deploy")
    def test_deploy_valid(self, p_deploy: MagicMock):
        # Test with a valid setup
        result = self.runner.invoke(
            e2cli.deploy, [str(self.test_folder), str(self.test_folder)]
        )
        self.assertEqual(result.exit_code, 0)
        p_deploy.assert_called_once_with(
            self.test_folder, self.test_folder, 0, 0, [], True, env=self.test_folder
        )

    @patch("e2clab.tasks.deploy")
    def test_deploy_app_conf(self, p_deploy: MagicMock):
        # Test with an app-conf argument
        result = self.runner.invoke(
            e2cli.deploy,
            [str(self.test_folder), str(self.test_folder), "--app_conf", "abc,xyz"],
        )
        self.assertEqual(result.exit_code, 0)
        p_deploy.assert_called_once_with(
            self.test_folder,
            self.test_folder,
            0,
            0,
            ["abc", "xyz"],
            True,
            env=self.test_folder,
        )

    @patch("e2clab.tasks.deploy")
    def test_deploy_invalid(self, p_deploy: MagicMock):
        # Testing an invalid setup
        invalid_folder = str(Path(__file__).resolve())
        result = self.runner.invoke(e2cli.deploy, [invalid_folder, invalid_folder])
        self.assertEqual(result.exit_code, 1)
        self.assertIn("Invalid setup, scenario not deployed.", result.stdout)

    @patch("e2clab.tasks.deploy")
    def test_deploy_invalid_scenarios(self, _):
        # Testing with invalid scenarios
        result = self.runner.invoke(
            e2cli.deploy,
            [
                str(self.test_folder),
                str(self.test_folder),
                "--scenarios_name",
                "test,abc",
            ],
        )
        self.assertEqual(result.exit_code, 1)
        self.assertIn("Invalid setup in test, scenario not deployed", result.stdout)

    @patch("e2clab.tasks.deploy")
    @patch("e2clab.utils.is_valid_setup")
    def test_deploy_valid_scenarios(self, p_is_valid: MagicMock, p_deploy: MagicMock):
        p_is_valid.return_value = True

        result = self.runner.invoke(
            e2cli.deploy,
            [
                str(self.test_folder),
                str(self.test_folder),
                "--scenarios_name",
                "test,abc",
            ],
        )
        self.assertEqual(result.exit_code, 0)
        # Second scenario call
        path2 = self.test_folder.resolve() / "abc"
        p_deploy.assert_called_with(
            path2,
            self.test_folder,
            0,
            0,
            [],
            True,
            env=path2,
        )
        p_is_valid.assert_called_with(path2, self.test_folder, Command.DEPLOY)

    @patch("e2clab.tasks.infra")
    def test_layers_services_valid(self, p_infra: MagicMock):
        # Testing a correct layers_services setup
        result = self.runner.invoke(
            e2cli.layers_services, [str(self.test_folder), str(self.test_folder)]
        )
        self.assertEqual(result.exit_code, 0)
        p_infra.assert_called_once_with(
            self.test_folder, self.test_folder, env=self.test_folder
        )

    @patch("e2clab.tasks.infra")
    def test_layers_services_invalid(self, p_infra: MagicMock):
        # Testing an invalid layers_services setup
        result = self.runner.invoke(
            e2cli.layers_services,
            [str(self.invalid_test_folder), str(self.invalid_test_folder)],
        )
        self.assertEqual(result.exit_code, 1)
        self.assertIn("Invalid setup,", result.stdout)

    @patch("e2clab.tasks.network")
    def test_network_valid(self, p_infra: MagicMock):

        result = self.runner.invoke(e2cli.network, [str(self.test_folder)])
        self.assertEqual(result.exit_code, 0)
        p_infra.assert_called_once_with(env=self.test_folder)

    @patch("e2clab.tasks.network")
    def test_network_invalid(self, p_infra: MagicMock):

        result = self.runner.invoke(e2cli.network, [str(self.invalid_test_folder)])
        self.assertEqual(result.exit_code, 1)
        self.assertIn("Invalid setup", result.stdout)

    @patch("e2clab.tasks.app")
    def test_workflow_valid(self, p_app: MagicMock):

        result = self.runner.invoke(e2cli.workflow, [str(self.test_folder), "prepare"])
        self.assertEqual(result.exit_code, 0)
        p_app.assert_called_once_with(task="prepare", env=self.test_folder)

    @patch("e2clab.tasks.app")
    def test_workflow_invalid(self, p_app: MagicMock):

        result = self.runner.invoke(
            e2cli.workflow, [str(self.invalid_test_folder), "prepare"]
        )
        self.assertEqual(result.exit_code, 1)
        self.assertIn("Invalid setup, workflow not launched", result.stdout)

    @patch("e2clab.tasks.app")
    @patch("e2clab.tasks.finalize")
    def test_workflow_valid_app_conf(self, p_finalize: MagicMock, p_app: MagicMock):

        result = self.runner.invoke(
            e2cli.workflow, [str(self.test_folder), "launch", "--app_conf", "test,opt"]
        )
        self.assertEqual(result.exit_code, 0)
        p_app.assert_called_with(task="launch", app_conf="opt", env=self.test_folder)
        p_finalize.assert_called_with(env=self.test_folder)

    @patch("e2clab.tasks.app")
    @patch("e2clab.tasks.finalize")
    def test_workflow_valid_app_conf_not_finalize(
        self, p_finalize: MagicMock, p_app: MagicMock
    ):

        result = self.runner.invoke(
            e2cli.workflow,
            [
                str(self.test_folder),
                "launch",
                "--app_conf",
                "test,opt",
                "--finalize_wf",
                False,
            ],
        )
        self.assertEqual(result.exit_code, 0)
        p_app.assert_called_with(task="launch", app_conf="opt", env=self.test_folder)
        p_finalize.assert_not_called()

    @patch("e2clab.tasks.app")
    def test_workflow_app_conf_prepare(self, p_app: MagicMock):

        result = self.runner.invoke(
            e2cli.workflow,
            [str(self.test_folder), "prepare", "--app_conf", "test,opt"],
        )
        self.assertEqual(result.exit_code, 1)
        self.assertIn("Can't use a configuration to prepare a workflow", result.stdout)

    @patch("e2clab.tasks.destroy")
    def test_destroy_valid(self, p_destroy: MagicMock):

        result = self.runner.invoke(e2cli.destroy, [str(self.test_folder)])
        self.assertEqual(result.exit_code, 0)
        p_destroy.assert_called_once()

    @patch("e2clab.tasks.destroy")
    def test_destroy_invalid(self, p_destroy: MagicMock):

        result = self.runner.invoke(e2cli.destroy, ["notafolder"])
        self.assertEqual(result.exit_code, 2)
        p_destroy.assert_not_called()

    @patch("e2clab.tasks.finalize")
    def test_finalize_valid(self, p_finalize: MagicMock):

        result = self.runner.invoke(e2cli.finalize, [str(self.test_folder)])
        self.assertEqual(result.exit_code, 0)
        p_finalize.assert_called_once_with(env=self.test_folder)

    @patch("e2clab.tasks.finalize")
    def test_finalize_invalid(self, p_finalize: MagicMock):

        result = self.runner.invoke(e2cli.finalize, [str(self.invalid_test_folder)])
        self.assertEqual(result.exit_code, 1)
        p_finalize.assert_not_called()

    def get_filepath_str(self, not_python_file: Path) -> str:
        file_path = str(not_python_file.resolve())
        return file_path
