import os
from pathlib import Path
from tempfile import NamedTemporaryFile

import e2clab.utils as utils
from e2clab.constants import Command, ConfFiles
from e2clab.errors import E2clabFileError
from e2clab.tests.unit import TestE2cLab


class TestUtils(TestE2cLab):
    def setUp(self):
        # Setup a temporary binary file.
        with NamedTemporaryFile(suffix=".bin", delete=False) as temp_file:
            # Write binary data to the temporary file
            temp_file.write(b"\x01\x02\x03\x04")

            # Get the path to the temporary file
            temp_file_path = temp_file.name

            temp_file.close()
            self.temp_binary_file = temp_file_path

    def tearDown(self):
        os.remove(self.temp_binary_file)

    def test_load_yaml(self):
        # Test opening a non existent file
        with self.assertRaises(E2clabFileError):
            utils.load_yaml_file(Path("notafile.yaml"))
        # Test opening a binary file
        with self.assertRaises(E2clabFileError):
            utils.load_yaml_file(Path(self.temp_binary_file))
        # Test opening an existing non-yaml file
        with self.assertRaises(E2clabFileError):
            file = Path(__file__).resolve().parent / "__init__.py"
            utils.load_yaml_file(file)
        # Test opening a valid yaml file
        valid_test_file = self.test_folder / ConfFiles.LAYERS_SERVICES
        self.assertIsNotNone(utils.load_yaml_file(valid_test_file))

    def test_validate_conf(self):
        layers_servies = self.test_folder / ConfFiles.LAYERS_SERVICES
        network = self.test_folder / ConfFiles.NETWORK
        workflow = self.test_folder / ConfFiles.WORKFLOW
        self.assertTrue(utils.validate_conf(layers_servies, "layers_services"))
        self.assertTrue(utils.validate_conf(network, "network"))
        self.assertTrue(utils.validate_conf(workflow, "workflow"))

        self.assertFalse(utils.validate_conf(Path("notafile"), "network"))

    def test_is_valid_setup(self):
        from e2clab.utils import is_valid_setup

        not_a_folder = Path("notafolder")
        is_a_valid_folder = self.test_folder
        not_a_valid_folder = Path(__file__).parent

        # Testing setting up invalid configuration folder
        self.assertFalse(is_valid_setup(not_a_folder, None, Command.DEPLOY, True))
        self.assertFalse(
            is_valid_setup(is_a_valid_folder, not_a_folder, Command.DEPLOY, True)
        )

        # Testing valid setup configurations
        self.assertTrue(is_valid_setup(is_a_valid_folder, None, Command.DEPLOY))
        self.assertTrue(is_valid_setup(is_a_valid_folder, None, Command.LYR_SVC))
        self.assertTrue(is_valid_setup(is_a_valid_folder, None, Command.NETWORK))
        self.assertTrue(is_valid_setup(is_a_valid_folder, None, Command.WORKFLOW))
        self.assertTrue(is_valid_setup(is_a_valid_folder, None, Command.FINALIZE))

        # Testing invalid setup configurations
        self.assertFalse(is_valid_setup(not_a_valid_folder, None, Command.DEPLOY))
        self.assertFalse(is_valid_setup(not_a_valid_folder, None, Command.LYR_SVC))
        self.assertFalse(is_valid_setup(not_a_valid_folder, None, Command.NETWORK))
        self.assertFalse(is_valid_setup(not_a_valid_folder, None, Command.WORKFLOW))
        self.assertFalse(is_valid_setup(not_a_valid_folder, None, Command.FINALIZE))

    def test_is_valid_task(self):
        # Testing valid task names
        self.assertTrue(utils.is_valid_task("Prepare"))
        self.assertTrue(utils.is_valid_task("launch"))
        self.assertTrue(utils.is_valid_task("FINALIZE"))

        # Testing an invalid task name
        self.assertFalse(utils.is_valid_task("NotATask"))
