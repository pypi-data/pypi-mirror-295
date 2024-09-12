import shutil
from pathlib import Path

import e2clab.optimizer as e2copt
from e2clab.constants import ConfFiles
from e2clab.errors import E2clabError
from e2clab.tests.unit import TestE2cLab


class MyOptimize(e2copt.Optimizer):

    def run(self):
        pass


class TestOptimizer(TestE2cLab):

    def test_optimizer_init(self):

        opt = MyOptimize(
            scenario_dir=self.test_folder,
            artifacts_dir=self.test_folder,
            duration=20,
            repeat=4,
        )

        self.assertEqual(opt.duration, 20)
        self.assertEqual(opt.repeat, 4)

        with self.assertRaises(E2clabError):
            opt = MyOptimize(
                scenario_dir=Path("notafolder"),
                artifacts_dir=Path("notafolder"),
            )

    def test_optimizer_prepare(self):

        opt = MyOptimize(
            scenario_dir=self.test_folder,
            artifacts_dir=self.test_folder,
        )

        opt.prepare()

        # Test that optimization dir exists
        self.assertTrue(opt.optimization_dir.exists())
        # Test file copy
        layers_services = opt.optimization_dir / ConfFiles.LAYERS_SERVICES
        network = opt.optimization_dir / ConfFiles.NETWORK
        workflow = opt.optimization_dir / ConfFiles.WORKFLOW
        for file in (layers_services, network, workflow):
            self.assertTrue(file.exists())

        shutil.rmtree(opt.optimization_dir)
