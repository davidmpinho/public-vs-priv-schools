# TODO: join all of these tests into one folder called "tests" inside stan_utils.

import unittest
import scipy.stats as stats
import pandas as pd
import numpy as np
from python_scripts.stan_utils import sim_helper as sh


class TestPriorSim(unittest.TestCase):
    def test_add_level(self):
        pass

if __name__ == '__main__':
    unittest.main()
