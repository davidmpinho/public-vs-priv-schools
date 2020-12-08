from python_scripts.stan_utils import sim_helper as sh


def sim_model_a(n_sims: int, levels: dict, seed: int):
    """
    Model with some hierarchical effects for the main variables (school quality,
    discipline and year difficulty), and the geospatial variable has no structure yet.
    """
    sim = sh.PriorSim(n_sims=n_sims, levels=levels, seed=seed)
    # Priors
    sim.add_prior('sigma_year', dist='halfnormal', loc=0, scale=0.6)
    sim.add_prior('sigma_grade', dist='halfnormal', loc=0, scale=0.6)
    sim.add_prior('beta_spatial', dist='normal', rep=True, loc=0, scale=0.5)
    sim.add_prior('beta_priv', dist='normal', rep=True, loc=0, scale=0.5)
    sim.add_prior('beta_edu', dist='normal', rep=True, loc=0, scale=0.5)
    sim.add_prior('beta_ses', dist='normal', rep=True, loc=0, scale=0.5)
    # Generative model for covariates
    sim.add_level('spatial', dist='normal', on_levels=['school'], loc=0, scale=1)
    sim.add_level('priv', dist='binomial', n=1, on_levels=['school'],
                  p=sh.logistic(0.4 * sim.df['spatial']))
    sim.add_level('edu', dist='normal', on_levels=['school', 'year'], scale=0.4,
                  loc=0.1 * sim.df['priv'] + 0.3 * sim.df['spatial'])
    sim.add_level('ses', dist='normal', on_levels=['school', 'year'], scale=0.4,
                  loc=(0.4 * sim.df['spatial'] + 0.2 * sim.df['priv']
                       + 0.2 * sim.df['edu']))
    # Main model
    sim.add_level('alpha_disc', dist='normal', on_levels=['disc'], loc=0, scale=0.5)
    sim.add_level('alpha_year', dist='normal', on_levels=['year'], loc=0,
                  scale=sim.priors['sigma_year'])
    sim.df['E_grade'] = (sim.df['alpha_disc'] + sim.df['alpha_year']
                         + sim.priors['beta_spatial'] * sim.df['spatial']
                         + sim.priors['beta_priv'] * sim.df['priv']
                         + sim.priors['beta_ses'] * sim.df['ses']
                         + sim.priors['beta_edu'] * sim.df['edu'])
    sim.add_level('grade', dist='normal', loc=sim.df['E_grade'],
                  on_levels=['school', 'disc', 'year'],
                  scale=sim.priors['sigma_grade'])
    sim.df = sim.df.groupby(['school', 'disc', 'n_sim'], as_index=False).mean()
    sim.update(seed=0, n_obs=True)
    return sim

def sim_model_b():
    # TODO: add GRF for the spatial effects
    pass

def sim_model_c():
    # TODO: add missing data
    pass

def sim_model_d():
    # TODO: add measurement error
    pass

def sim_model_e():
    # Optional
    # TODO: add interactions to show that the total effect is still recovered
    pass

def sim_model_f():
    # Optional
    # TODO: add splines
    pass

def sim_model_g():
    # Optional
    # TODO: add student_t distributions where appropriate
    pass

if __name__ == '__main__':
    # TODO
    pass




