import pandas as pd
import numpy as np
import scipy.stats as stats
import itertools
from asteval import Interpreter


class PriorSim:
    """
    Each time a variable is added, the seed increases by one to avoid
    repeated results.
    TODO: the API should be simplified a lot. Think about doing this with the tidyverse. 
    TODO: probably needs an attributed named "aux_data" for distance matrixes and such
    """
    def __init__(self, n_sims, levels=None, seed=1):
        if levels is None:
            levels = {}
        levels['n_sim'] = n_sims
        level_values = list(levels.values())
        levels_index = itertools.product(*[np.arange(1, x+1) for x in level_values])
        self.df = pd.DataFrame(levels_index, columns=levels.keys())
        self.levels = levels
        self.n_obs = self.df.shape[0]
        self.n_sims = n_sims
        self.seed = seed
        self.ast_eval = Interpreter()
        self._add_asteval_functions()

    def add_level(self, name: str, dist: str, on_levels: list, **kwargs):
        """
        Allows you to specify a level that is not always the same size
        (e.g., different number of classes per school).  
        """
        pass

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
                values = sim_linear(dist=dist, size=self.df.shape[0],
                                    seed=self.seed, **kwargs)
                self.df.loc[:, n] = values
            elif isinstance(on_levels, list):
                on_levels_var = on_levels + ['n_sim']
                kwargs = self._eval_formulas(kwargs)
                self._adjust_param_shape_to_levels(kwargs=kwargs, on_levels=on_levels_var)
                mask = [c in on_levels_var for c in self.df.columns]
                unique_df = self.df.loc[:, mask].drop_duplicates(ignore_index=True)
                unique_df.loc[:, n] = sim_linear(dist=dist, size=unique_df.shape[0],
                                                    seed=self.seed, **kwargs)
                self.df = pd.merge(self.df, unique_df, on=on_levels_var)
            else:
                warning = "'on_levels' needs to be a list with column names or of NoneType."
                assert isinstance(on_levels, list), warning
            self.update_attrs(add_to_seed=1, new_var=n)
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
        # TODO: leave this for another time
        pass

    def add_sem(self):
        """Structural equations (formulas like blavaan, maybe)"""
        pass

    def add_sum(self, name: str, formula: str):
        # TODO: add option for multiple names
        values = self._eval_formulas(formula)
        self.df.loc[:, name] = values
        self.update_attrs(add_to_seed=0, new_var=name)
        return self

    def add_prior(self, name, dist: str, on_levels=[], **kwargs):
        """Adds a prior. Works identically to add_var, except that on_levels is
          an empty list by default. This makes the method draw one sample
          per simulation instead of one sample per row (which is add_var's default)."""
        self.add_var(name=name, dist=dist, on_levels=on_levels, **kwargs)
        return self

    def _eval_formulas(self, x: str or dict):
        """ Evaluate any formulas that are in kwargs' variables."""
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

    def _adjust_param_shape_to_levels(self, kwargs, on_levels):
        for key, values in kwargs.items():
            if not isinstance(values, (int, float)):
                index_select = self.df[on_levels].drop_duplicates().index
                if len(values) == self.df.shape[0]:
                    kwargs[key] = values[index_select]
                if len(kwargs[key]) != len(index_select):
                    kwargs[key] = np.repeat(values, len(index_select) / len(values))
        return kwargs

    def _add_asteval_functions(self):
        # TODO: add a method to create new functions
        self.ast_eval("def logit(x):\n\t"
                      + "return log(x / (1-x))\n"
                      + "def logistic(x):\n\t"
                      + "return 1 / (1+exp(-x))\n"
                      + "def standardize(x):\n\t"
                      + "return (x - mean(x)) / std(x)")

    def update_attrs(self, add_to_seed: int=0, n_obs=True, new_var=None):
        self.seed += add_to_seed
        self.df = self.df.reset_index(drop=True)  # TODO: better remove to not hide errors?
        if n_obs:
            self.n_obs = int(self.df.shape[0] / self.n_sims)
        if new_var:
            self.ast_eval.symtable[new_var] = self.df[new_var]

    def copy(self):
        pass

    def __repr__(self):
        return repr(self.df)

    def __str__(self):
        return repr(self.df)


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
        lamb = 1/kwargs.get('scale')
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

def standardize(df: pd.DataFrame or pd.Series, cols):
    df = df.copy()
    df.loc[:, cols] = df.loc[:, cols].apply(func=lambda x: (x - x.mean()) / x.std())
    return df
