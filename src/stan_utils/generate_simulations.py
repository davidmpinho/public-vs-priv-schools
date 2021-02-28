from src.stan_utils import sim_helper as sh


def sim_model_s1_a(n_sims: int, seed: int = 1):
    """
    Model where each school's grade is dictated by hierarchical effects on the
    year of the exam, county, and school. In my Stan model, I aggregate all
    years to make the model simpler, thus ignoring year-to-year variability,
    which is why I perform the 'groupby' operations at the end.

    There is one confounder: counties with more schools have better socioeconomic conditions.
    """
    # Create the levels (i.e., hierarchical structure)
    sim = sh.PriorSim(n_sims=n_sims, levels={'county': 300}, seed=seed)
    (sim.add_level('school', n=800, method='random')
        .add_level('year', n=4, for_each=['school'], rep_index=True)
    # Priors
        .add_prior(['sigma_year', 'sigma_school', 'sigma_county', 'sigma_grade'],
                   'halfnormal', loc=0, scale=0.5)
        .add_prior(['beta_priv', 'beta_edu', 'beta_ses'],
                   'normal', loc=0, scale=0.5)
    # Auxiliary quantity for the confounding
        .add_groupby_var('schools_by_county', groupby_vars=['county'],
                         select='school', func=lambda x: len(x) / 4)
    # Generative model for covariates with confounder
        .add_var('alpha_county', 'normal', on_levels=['county'],
                 loc='sigma_county * standardize(schools_by_county)', scale=0)
        .add_var('priv', 'binomial', on_levels=['school'], n=1,
                 p='logistic(0.5 * alpha_county)')
        .add_var('edu', 'normal', on_levels=['school', 'year'],
                 loc='0.1 * priv + 0.3 * alpha_county', scale=0.4)
        .add_var('ses', 'normal', on_levels=['school', 'year'],
                 loc='0.2 * priv + 0.4 * alpha_county + 0.2 * edu', scale=0.4)
        .add_var('alpha_year', 'normal', on_levels=['year'], loc=0, scale='sigma_year')
     # Generative model for the dependent variable
        .add_sum('mu_grade', formula=('alpha_year + alpha_county '
                                      '+ beta_priv * priv '
                                      '+ beta_ses * ses '
                                      '+ beta_edu * edu'))
        .add_var('grade', 'normal', loc='mu_grade', scale='sigma_grade'))
    # Data for the model that I will actually fit
    sim.data.groupby(['school', 'sim'], as_index=False).mean() # TODO: make a method for this?
    sim.update_attrs(n_obs=True) # TODO: make a method to update all
    return sim

def sim_model_s1_b(n_sims: int, seed: int):
    """
    Same as model A, but now it has spatial effects ("between-neighborhood counfounders",
    as they talk about in https://journals.sagepub.com/doi/10.1177/0081175013490188,
    but look at the other Gelman et al. paper on adding structure to MRP).
    """
    # For the actual model, instead of GP use NNGP: https://arxiv.org/pdf/1802.00495.pdf
    # The code for GPs should look something like (but add_gp would
    # also allow for time series depending on how many coords I pass):
    """
    sim.add_var(['coord_x', 'coord_y'], 'uniform', 0, 1)
    sim.add_var('sigma_gp', on_levels=['school'], 'normal', 0, 1)
    sim.add_var('phi', on_levels=['school'], 'normal', 0, 1)
    sim.add_gp('spatial_confounder', on_levels=['school'], method='eucledian_norm',
               distance=['coord_x', 'coord_y'], mu=<formula for 'spatial_confounder' above>,
               var='sigma_gp', phi=...) 
    TODO: in method='custom' let the user specify the formula, something like:
        method_func='alpha**2 * phi * distance(coord_x, coord_y)**2 ...'
    """

def sim_model_s1_c():
    # TODO: add missing data and measurement error to predictors.
    pass

def sim_model_s1_d():
    # TODO: add important interactions
    pass

def sim_model_s1_e():
    # TODO: add splines
    pass

def sim_model_s2_a():
    # TODO: mixture-type model with missingness + hierarchy based on school
    pass

def sim_model_s2_b():
    # TODO: non-linearity
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




