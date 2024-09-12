import e2clab.constants as e2cconst
from e2clab.tests.unit import TestE2cLab


class TestConstants(TestE2cLab):

    def test_enum(self):

        class TestClass(e2cconst.ExtEnum):
            A = 1
            B = 2
            C = "test"
            D = 4
            E = 5

        expect = [1, 2, "test", 4, 5]
        res = TestClass.value_list()
        self.assertEqual(expect, res)
