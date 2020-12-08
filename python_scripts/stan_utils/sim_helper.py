import pandas as pd
import numpy as np
import scipy.stats as stats
import itertools


class PriorSim:
    """
    TODO: the API should be simplified a lot.
    Each time a variable is added, the seed increases by one to avoid
    repeated results.
    """
    def __init__(self, n_sims, levels=None, seed=1):
        if levels is None:
            levels = {}
        levels['n_sim'] = n_sims
        level_values = list(levels.values())
        levels_index = itertools.product(*[np.arange(1, x+1) for x in level_values])
        self.df = pd.DataFrame(levels_index, columns=levels.keys())
        self.levels = levels
        self.priors = {}
        self.n_obs = self.df.shape[0]
        self.n_sims = n_sims
        self.seed = seed

    def add_level(self, name: str, dist: str, on_levels=None, **kwargs):
        # This is meant to crete a 'level' in a multilevel model.
        # The mean is assumed to be centered on zero (I might have to change this)
        #
        if on_levels is None:
            # TODO: this part might have to be passed to another method.
            #  Let on_levels=None be equal to specifying every level
            #  in self.levels.keys()
            values = sim_linear(dist=dist, size=self.df.shape[0],
                                seed=self.seed, **kwargs)
            self.df.loc[:, name] = values
        elif isinstance(on_levels, list):
            # TODO: make 'adjust_param_shape' function for this
            on_levels += ['n_sim']
            for key, values in kwargs.items():
                if not isinstance(values, (int, float)):
                    index_select = self.df[on_levels].drop_duplicates().index
                    if len(values) == self.df.shape[0]:
                        kwargs[key] = values[index_select]
                    if len(kwargs[key]) != len(index_select):
                        kwargs[key] = np.repeat(values, len(index_select) / len(values))
            mask = [c in on_levels for c in self.df.columns]
            unique_df = self.df.loc[:, mask].drop_duplicates().reset_index(drop=True)
            unique_df.loc[:, name] = sim_linear(dist=dist, size=unique_df.shape[0],
                                                seed=self.seed, **kwargs)
            self.df = pd.merge(self.df, unique_df, on=on_levels)
        else:
            warning = "'on_levels' needs to be a list with column names or of NoneType."
            assert isinstance(on_levels, list), warning
        self.update(seed=1)

    def add_spatial(self, name, method: str, index_cols: list, method_args: dict):
        pass

    def add_error(self, name, dist):
        pass

    def add_missing(self, name, dist):
        pass

    def add_missing_data(self):
        pass

    def add_time_series(self, name: str):
        # TODO: leave this for another time
        pass

    def add_prior(self, name: str, dist: str, on_levels=None, rep=False, **kwargs):
        # TODO: add feature allowing for multiple priors at the same
        #  time by passing multiple names
        if (on_levels == []) or (on_levels is None):
            new_prior = ModelPrior(n_sims=self.n_sims, levels={}, seed=self.seed)
            new_prior.add_level(name=name, dist=dist, **kwargs)
            self.priors[name] = new_prior.df[name].to_numpy()
        elif isinstance(on_levels, list):
            levels = dict(self.df.loc[:, on_levels].max())
            new_prior = ModelPrior(n_sims=self.n_sims, levels=levels, seed=self.seed)
            new_prior.add_level(name=name, dist=dist, **kwargs)
            self.priors[name] = new_prior.df[name].to_numpy()
        else:
            warning = "'on_levels' needs to be a list with column names or of NoneType."
            assert isinstance(on_levels, list), warning

        if rep:
            repeat = len(self.df) / len(self.priors[name])
            self.priors[name] = np.repeat(self.priors[name], repeat)
        self.update(seed=1)

    @staticmethod
    def adjust_length(d: dict, rep: int):
        for key in d.keys():
            try:
                len_key = len(d[key])
            except TypeError:
                d[key] = pd.Series(d[key])
                len_key = len(d[key])
            d[key] = d[key].iloc[np.repeat(np.arange(len_key), int(rep/len_key))]
        return d

    @staticmethod
    def tile_by_level(df: pd.DataFrame, n_groups: int, len_prev_levels, n_sims: int):
        rows_1_sim = n_groups * len_prev_levels
        new_df = pd.DataFrame(index=np.arange(rows_1_sim * n_sims), columns=df.columns)
        for i in np.arange(n_sims):
            index_new = np.arange(start=rows_1_sim * i, stop=rows_1_sim * (i+1))
            index_old = np.arange(start=n_groups * i, stop=n_groups * (i+1))
            new_df.iloc[index_new, :] = (df.iloc[np.tile(index_old, len_prev_levels)]
                                           .set_index(index_new))
        return new_df

    def update(self, seed: int, n_obs=True):
        self.seed += seed
        self.df = self.df.reset_index(drop=True)
        if n_obs:
            self.n_obs = int(self.df.shape[0] / self.n_sims)

    def __repr__(self):
        return repr(self.df)

    def __str__(self):
        return repr(self.df)

class ModelPrior(PriorSim):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

def sim_linear(dist: str, size: int, seed: int, **kwargs):
    # TODO: it is better to refactor? Just let the user pass these function to the PriorSim?
    if (dist == 'normal') | (dist == 'halfnormal'):
        data = stats.norm.rvs(size=size, loc=kwargs.get('loc'), scale=kwargs.get('scale'),
                              random_state=seed)
        if dist == 'halfnormal':
            # TODO: mmaybe
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
    return np.exp(x) / (1+np.exp(x))

def standardize(df: pd.DataFrame or pd.Series, cols):
    df = df.copy()
    df.loc[:, cols] = df.loc[:, cols].apply(func=lambda x: (x - x.mean()) / x.std())
    return df
