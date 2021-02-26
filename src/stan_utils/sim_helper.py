import pandas as pd
import numpy as np
import scipy.stats as stats
import itertools
import copy
from asteval import Interpreter
from typing import Callable


class PriorSim:
    """
    Each time a variable is added, the seed increases by one to avoid
    repeated results.
    TODO: probably needs an attribute named "aux_data" for distance matrixes and such
    """
    def __init__(self, n_sims, levels=None, seed=1):
        self.levels = copy.deepcopy(levels)
        if self.levels is None:
            self.levels = {}
        self.levels['sim'] = n_sims
        level_values = list(self.levels.values())
        levels_index = itertools.product(*[np.arange(1, x+1) for x in level_values])
        self.data = pd.DataFrame(levels_index, columns=self.levels.keys())
        self.n_obs = self.data.shape[0]
        self.n_sims = n_sims
        self.seed = seed
        self.ast_eval = Interpreter()
        self._add_asteval_functions()

    def add_level(self, name: str, n: int, for_each: list=['sim'],
                  rep_index=False, method='uniform'):
        """
        Allows you to specify a level that is not always the same size
        (e.g., different number of classes per school).
        """
        # TODO: refactor this method, perhaps by ensuring that the levels are already sorted
        #   and then taking advantage of that fact.
        # NOTE: remember that the loops with masks are there for the sake of robustness.
        if 'sim' not in for_each:
            for_each += ['sim']
        unique_comb = self.data.loc[:, for_each].drop_duplicates()
        new_index = np.arange(0, n * unique_comb.shape[0])
        new_data = pd.DataFrame(index=new_index, columns=self.data.columns)

        i_last_end = 0
        sim_count = np.zeros(self.n_sims)
        for i, row_vals in enumerate(unique_comb.iterrows()):
            mask = (self.data.loc[:, for_each] == row_vals[1]).sum(axis=1) == len(for_each)
            len_index = mask[mask].shape[0]
            reps_per_row = self._get_rep_per_row(method=method, n=n, len_slice=len_index)
            index_w_reps = np.repeat(mask[mask].index, reps_per_row)
            i_curr_end = i_last_end + np.sum(reps_per_row)

            new_data.loc[i_last_end:(i_curr_end-1), self.data.columns] = (
                self.data.loc[index_w_reps, self.data.columns]
                       .set_index(np.arange(i_last_end, i_curr_end)))
            if rep_index:
                new_data.loc[i_last_end:(i_curr_end-1), name] = np.arange(1, len_index*n+1)
            else:
                curr_sim = int(self.data.loc[mask, 'sim'].unique())
                level_index = np.arange(1, i_curr_end-i_last_end+1) + sim_count[curr_sim-1]
                sim_count[curr_sim-1] += len(level_index)
                new_data.loc[i_last_end:(i_curr_end-1), name] = level_index
            i_last_end += i_curr_end - i_last_end
        self.data = new_data.astype(np.int64)
        self.levels[name] = self.data[name].max()
        self.update_attrs(add_to_seed=1, n_obs=True, new_var=name)
        return self

    def add_var(self, name: str or list, dist: str, on_levels=None, **kwargs):
        """
        Create a variable (becomes a column in the dataframe). 
        The hierarchy is specified with `on_levels`.
        """
        if isinstance(name, str):
            name = [name]
        for n in name:
            if on_levels is None:
                kwargs = self._eval_formulas(kwargs)
                values = sim_linear(dist=dist, size=self.data.shape[0],
                                    seed=self.seed, **kwargs)
                self.data.loc[:, n] = values
            elif isinstance(on_levels, list):
                on_levels_var = on_levels + ['sim']
                kwargs = self._eval_formulas(kwargs)
                self._adjust_param_shape_to_levels(kwargs=kwargs, on_levels=on_levels_var)
                mask = [col in on_levels_var for col in self.data.columns]
                unique_data = self.data.loc[:, mask].drop_duplicates(ignore_index=True)
                unique_data.loc[:, n] = sim_linear(dist=dist, size=unique_data.shape[0],
                                                    seed=self.seed, **kwargs)
                self.data = pd.merge(self.data, unique_data, on=on_levels_var)
            else:
                warning = "'on_levels' needs to be a list with column names or None."
                assert isinstance(on_levels, list), warning
        self.update_attrs(add_to_seed=0, new_var=name)
        return self

    def add_prior(self, name: str or list, dist: str, on_levels: list = [], **kwargs):
        """Adds a prior. Works identically to add_var, except that on_levels is
          an empty list by default. This makes the method draw one sample
          per simulation instead of one sample per row (which is add_var's default)."""
        self.add_var(name=name, dist=dist, on_levels=on_levels, **kwargs)
        return self

    def add_groupby_var(self, name: str, groupby_vars: list, select: str,
                        func: str or Callable):
        if 'sim' not in groupby_vars:
            groupby_vars += ['sim']
        values = (self.data.groupby(groupby_vars, as_index=False)[select]
                           .transform(func=func)
                           .to_numpy())
        self.data.loc[:, name] = values
        self.update_attrs(new_var=name)
        return self

    def add_spatial(self, name, method: str, index_cols: list, method_args: dict):
        pass

    def add_error(self, to_var, dist, on_levels):
        # TODO: Name the new variable "{}_w_error"
        pass

    def add_miss(self, to_var, dist, on_levels):
        # TODO: Name the new variable "{}_w_miss"
        pass

    def add_ts(self, name: str):
        """ Add time series. This should abstract all the indexing that one would need
        to do when using these models."""
        # TODO: leave this for later
        pass

    def add_sem(self):
        """Structural equations (formulas like blavaan, maybe)"""
        pass

    def add_sum(self, name: str, formula: str):
        # TODO: add option for multiple names
        values = self._eval_formulas(formula)
        self.data.loc[:, name] = values
        self.update_attrs(new_var=name)
        return self


    def _eval_formulas(self, x: str or dict) -> float or int:
        """ Evaluate any formulas that are in variables (typically in the
        ones specified in 'kwargs')."""
        if isinstance(x, dict):
            for key, value in x.items():
                if isinstance(value, (int, float)):
                    pass
                elif isinstance(value, str):
                    # TODO: add try/except if something in 'value' is not recognized.
                    x[key] = self.ast_eval(value)
        elif isinstance(x, str):
            x = self.ast_eval(x)
        return x

    def _adjust_param_shape_to_levels(self, kwargs: dict, on_levels: list) -> dict:
        for key, values in kwargs.items():
            if not isinstance(values, (int, float)):
                index_select = self.data[on_levels].drop_duplicates().index
                if len(values) == self.data.shape[0]:
                    kwargs[key] = values[index_select]
                if len(kwargs[key]) != len(index_select):
                    kwargs[key] = np.repeat(values, len(index_select) / len(values))
        return kwargs

    def _get_rep_per_row(self, method: str, n: int, len_slice: int) -> np.array:
        # Supposes that repeated indexes are are ordered.
        np.random.seed(seed=self.seed)
        counts = np.ones(len_slice)
        size = n - len_slice
        positions = np.arange(len_slice)
        if method == 'random':
            if size > 0:
                rand_vals = np.random.choice(positions, size=size)
                counts += np.array([np.sum(x == rand_vals) for x in positions])
        elif method == 'uniform':
            # TODO: test
            add_to_all = size // len_slice
            counts += add_to_all
            size -= add_to_all * len_slice
            if size > 0:
                rand_vals = np.random.choice(positions, size=size)
                counts += np.array([np.sum(x == rand_vals) for x in positions])
        elif method == 'skewed':
            # TODO: use a Dirichlet distribution
            pass
        return counts

    def _add_asteval_functions(self):
        # TODO: add a method to add functions to ast_eval
        self.ast_eval("def logit(x):\n\t"
                      + "return log(x / (1-x))\n"
                      + "def logistic(x):\n\t"
                      + "return 1 / (1+exp(-x))\n"
                      + "def standardize(x):\n\t"
                      + "return (x - mean(x)) / std(x)")

    def update_attrs(self, add_to_seed: int=0, n_obs: bool=True, new_var: str=None):
        self.seed += add_to_seed
        self.data = self.data.reset_index(drop=True)  # TODO: better remove to not hide errors
        if n_obs:
            self.n_obs = int(self.data.shape[0] / self.n_sims)
        if new_var:
            if isinstance(new_var, list):
                for var in new_var:
                    self.ast_eval.symtable[var] = self.data[var]
            elif isinstance(new_var, str):
                self.ast_eval.symtable[new_var] = self.data[new_var]

    def copy(self):
        return copy.copy(self)

    def __repr__(self):
        return repr(self.data)

    def __str__(self):
        return repr(self.data)


def sim_linear(dist: str, size: int, seed: int, **kwargs):
    if (dist == 'normal') | (dist == 'halfnormal'):
        data = stats.norm.rvs(size=size, loc=kwargs.get('loc'), scale=kwargs.get('scale'),
                              random_state=seed)
        if dist == 'halfnormal':
            # TODO: make this more general. Have a 'lower' and an 'upper' argument with a while-loop
            data = np.abs(data)
    elif dist == 'binomial':
        data = stats.binom.rvs(size=size, n=kwargs.get('n'),
                               p=kwargs.get('p'), random_state=seed)
    elif dist == 'student_t':
        data = stats.t.rvs(size=size, loc=kwargs.get('loc'), df=kwargs.get('df'),
                           scale=kwargs.get('scale'), random_state=seed)
    elif dist == 'exponential':
        lamb = 1 / kwargs.get('scale')
        data = stats.expon.rvs(size=size, loc=0, scale=lamb, random_state=seed)
    elif dist == 'gamma':
        data = stats.gamma.rvs(size=size, a=kwargs.get('alpha'),
                               scale=1/kwargs.get('beta'), random_state=seed)
    else:
        print(('Distribution not supported in sim_linear function.'
               + 'Setting values as nan.'))
        data = np.nan
    return data

def sim_spatial(method, size, seed, **kwargs):
    if method == 'linear':
        data = sim_linear(size=size, seed=seed, **kwargs)
    elif method == 'grf':
        # Gaussian random field
        pass
    return data

def sim_splines():
    pass

def sim_data_series():
    pass

def logit(x):
    return np.log(x/(1-x))

def logistic(x):
    return 1 / (1+np.exp(-x))

def standardize(data: pd.DataFrame or pd.Series, cols):
    data = data.copy()
    data.loc[:, cols] = data.loc[:, cols].apply(func=lambda x: (x - x.mean()) / x.std())
    return data
