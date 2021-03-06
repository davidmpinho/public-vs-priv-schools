from src.stan_utils import generate_simulations as gsim
import cmdstanpy as csp
import os


csp.install_cmdstan()
PARAMS = dict(
    n_sims=5,
    seed=1,
    path_models=os.getcwd() + '/stan_models/',
    path_samples=os.getcwd() + '/model_validation/posterior_samples/'
)

# Model A
ma_obj = csp.CmdStanModel(stan_file=PARAMS['path_models'] + 'model_a_sim.stan')
ma_data = gsim.sim_model_s1_a(n_sims=PARAMS['n_sims'], seed=PARAMS['seed'])

for i in range(1, PARAMS['n_sims'] + 1):
    # TODO: turn at least some of this into a function
    mask_rows = (ma_data.df['sim'] == i)
    mask_cols = [col != 'sim' for col in ma_data.df.columns]
    data_fit = ma_data.df.loc[mask_rows, mask_cols].to_dict(orient='list')
    data_fit['x'] = ma_data.df.loc[mask_rows, ['priv', 'ses', 'edu']
                                  ].to_numpy().tolist()
    data_fit['P'] = 3
    data_fit['N'] = ma_data.n_obs
    data_fit['N_county'] = ma_data.levels['county']
    data_fit['N_school'] = ma_data.levels['school']

    ma_fit = ma_obj.sample(data=data_fit, chains=4, parallel_chains=4,
                           iter_warmup=1000, iter_sampling=1000, seed=1,
                           save_diagnostics=False, adapt_delta=0.95,
                           output_dir=PARAMS['path_samples'] + '/model_a/',
                           show_progress=True, max_treedepth=15)
    ma_fit.summary().to_csv((PARAMS['path_samples'] + '/model_a/model_a_summary_'
                             + str(i) + '.txt'), float_format='%.4f')
    with open(PARAMS['path_samples'] + '/model_a/model_a_diagnose_'
              + str(i) + '.txt', 'w') as f:
        f.write(ma_fit.diagnose())


# Model B

# ...

