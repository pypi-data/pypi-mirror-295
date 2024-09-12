import subprocess
import traceback
import unittest
from pathlib import Path

import numpy as np


def np_sa(x):
    y = np.ones_like(x)
    _nonzero_indices = x != 0
    x_nz = x[_nonzero_indices]
    y[_nonzero_indices] = np.sin(x_nz) / x_nz
    return y


class BuildAgainstTest(unittest.TestCase):
    def setUp(self) -> None:
        self.x = np.arange(-10, 10, 0.5)
        self.y = np_sa(self.x)

    def test_build(self):
        c_src_path = Path(__file__).parent / "c_src.pyx"
        cmd = f"cythonize -i {c_src_path}"
        try:
            result = subprocess.run(cmd,
                                    capture_output=True,
                                    check=True, shell=True)
        except subprocess.CalledProcessError:
            print(f"Cannot execute command: {cmd}. "
                  "Please check the existence of `cythonize`.")
            return

        from .c_src import my_sa

        self.assertEqual(
            my_sa(self.x.tolist()),
            self.y.tolist()
        )

    def test_python_import_1(self):
        from cypkgdemo.sa import sa
        self.assertEqual(sa(0), 1)
        self.assertEqual(sa(1), np.sin(1))
        self.assertTrue(
            np.allclose(
                sa(self.x),
                self.y
            )
        )

    # ERROR: import * only allowed at module level
    # def test_python_import_2(self):
    #     from cypkgdemo.sa import *
    #     self.assertEqual(sa(0), 1)
    #     self.assertEqual(sa(1), np.sin(1))
    #     self.assertTrue(
    #         np.allclose(
    #             sa(self.x),
    #             self.y
    #         )
    #     )

    def test_python_import_3(self):
        from cypkgdemo import sa as sa_module
        self.assertEqual(sa_module.sa(0), 1)
        self.assertEqual(sa_module.sa(1), np.sin(1))
        self.assertTrue(
            np.allclose(
                sa_module.sa(self.x),
                self.y
            )
        )

    # ERROR: import * only allowed at module level
    # def test_python_import_4(self):
    #     from cypkgdemo import *
    #     self.assertEqual(sa.sa(0), 1)
    #     self.assertEqual(sa.sa(1), np.sin(1))
    #     self.assertTrue(
    #         np.allclose(
    #             sa.sa(self.x),
    #             self.y
    #         )
    #     )

    def test_python_import_5(self):
        import cypkgdemo
        self.assertEqual(cypkgdemo.sa.sa(0), 1)
        self.assertEqual(cypkgdemo.sa.sa(1), np.sin(1))
        self.assertTrue(
            np.allclose(
                cypkgdemo.sa.sa(self.x),
                self.y
            )
        )
