from src.stan_utils import sim_helper as sh


def sim_model_s1_a(n_sims: int, levels: dict, seed: int):
    """
    Model with some hierarchical effects for the main variables (school quality,
    discipline and year difficulty), and the geospatial variable has no structure yet.
    """
    sim = sh.PriorSim(n_sims=n_sims, levels=levels, seed=seed)
    # Priors
    sim = (sim.add_prior(['sigma_year', 'sigma_grade'], 'halfnormal', loc=0, scale=0.6)
              .add_prior(['beta_spatial', 'beta_priv', 'beta_edu', 'beta_ses'],
                         'normal', loc=0, scale=0.6))

    # Generative model for covariates
    sim = (sim.add_var('spatial', 'normal', on_levels=['school'], loc=0, scale=1)
              .add_var('priv', 'binomial', on_levels=['school'], n=1,
                       p='0.2 * logistic(spatial)')
              .add_var('edu', 'normal', on_levels=['school', 'year'],
                       loc='0.1 * priv + 0.3 * spatial', scale=0.4)
              .add_var('ses', 'normal', on_levels=['school', 'year'],
                       loc='0.2 * priv + 0.4 * spatial + 0.2 * edu', scale=0.4))

    # Generative model for the dependent variable
    sim = (sim.add_var('alpha_disc', 'normal', on_levels=['disc'], loc=0, scale=0.5)
              .add_var('alpha_year', 'normal', on_levels=['year'], loc=0, scale='sigma_year')
              .add_sum('loc_grade', formula=('alpha_disc + alpha_year '
                                             '+ beta_spatial * spatial '
                                             '+ beta_priv * priv '
                                             '+ beta_ses * ses '
                                             '+ beta_edu * edu'))
              .add_var('grade', 'normal', loc='loc_grade', scale='sigma_grade'))
    sim.df = sim.df.groupby(['school', 'disc', 'n_sim'], as_index=False).mean()  # TODO: should year be here?
    sim.update_attrs(add_to_seed=0, n_obs=True)
    return sim

def sim_model_s1_b():
    # TODO: add GRF for the spatial effects
    pass

def sim_model_s1_c():
    # TODO: add missing data and measurement error
    pass

def sim_model_s1_d():
    # TODO: add important interactions + student_t outcome
    pass

def sim_model_s1_e():
    # TODO: add splines or a MARS-like model 'tilted' towards linear relationships
    # (not sure, the random walk specification may be less problematic in general)
    pass

def sim_model_s2_a():
    # TODO: mixture-type model with missingness + hierarchy based on school
    pass

def sim_model_s2_b():
    # TODO: non-linearity (maybe an ordered logistic?)
    pass

def sim_model_s2_c():
    # TODO: make that non-linear relationship hierarchical
    pass

def sim_model_s2_d():
    # TODO: additional variables to eliminate measurement error (discipline, sex, etc.)
    # See how far you can push it.
    pass

if __name__ == '__main__':
    # TODO
    pass




