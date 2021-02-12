# TODO: join all of these tests into one folder called "tests" inside stan_utils.

import unittest
import scipy.stats as stats
import pandas as pd
import numpy as np
from python_scripts.stan_utils import sim_helper as sh


class TestSimLinear(unittest.TestCase):
    def test_normal_dist(self):
        data_test = sh.sim_linear(size=5, dist='normal', loc=0, scale=1, seed=1)
        data = stats.norm.rvs(size=5, loc=0, scale=1, random_state=1)
        self.assertTrue(np.testing.assert_allclose(data_test, data) is None)

    # TODO: tests for other distributions.

    def test_unknown_dist(self):
        data = sh.sim_linear(size=10, dist='hello', loc=0, scale=1, seed=1)
        self.assertTrue(np.isnan(data))

class TestPriorSim(unittest.TestCase):
    def test_add_level(self):
        pass




if __name__ == '__main__':
    unittest.main()
