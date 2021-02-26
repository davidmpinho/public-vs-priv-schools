functions{
  real nngp_lpdf(vector Y, vector X_beta, real sigmasq, real tausq,
                 real phi, matrix NN_dist, matrix NN_distM, int[,] NN_ind,
                 int N, int M) {
    /* Response NNGP model, source: github.com/LuZhangstat/NNGP_STAN/ */
    vector[N] V;
    vector[N] YXb = Y - X_beta;
    vector[N] U = YXb;
    real kappa_p_1 = tausq / sigmasq + 1;
    int dim;
    int h;

    for (i in 2:N) {
      matrix[ i < (M + 1) ? (i - 1) : M, i < (M + 1) ? (i - 1): M]
      iNNdistM;
      matrix[ i < (M + 1) ? (i - 1) : M, i < (M + 1) ? (i - 1): M]
      iNNCholL;
      vector[ i < (M + 1) ? (i - 1) : M] iNNcorr;
      vector[ i < (M + 1) ? (i - 1) : M] v;
      row_vector[i < (M + 1) ? (i - 1) : M] v2;
      dim = (i < (M + 1))? (i - 1) : M;

      if(dim == 1) {
        iNNdistM[1, 1] = kappa_p_1;
      }
      else {
          h = 0;
          for (j in 1:(dim - 1)) {
              for (k in (j + 1):dim) {
                  h = h + 1;
                  iNNdistM[j, k] = exp(- phi * NN_distM[(i - 1), h]);
                  iNNdistM[k, j] = iNNdistM[j, k];
              }
          }
          for(j in 1:dim) {
              iNNdistM[j, j] = kappa_p_1;
          }
      }

      iNNCholL = cholesky_decompose(iNNdistM);
      iNNcorr = to_vector(exp(- phi * NN_dist[(i - 1), 1: dim]));

      v = mdivide_left_tri_low(iNNCholL, iNNcorr);
      V[i] = kappa_p_1 - dot_self(v);
      v2 = mdivide_right_tri_low(v', iNNCholL);
      U[i] = U[i] - v2 * YXb[NN_ind[(i - 1), 1:dim]];
    }
    V[1] = kappa_p_1;

    return - 0.5 * ( 1 / sigmasq * dot_product(U, (U ./ V)) +
                    sum(log(V)) + N * log(sigmasq));
  }
}
data {
  int<lower=1> N;
  int<lower=1> K;
  int<lower=1> P;
  vector[N] y;
  matrix[N, P + 1] x;                          // Number of predictors (+ constant)
  int nn_ind[N - 1, K];                        //
  matrix[N - 1, K] nn_dist;                    //
  matrix[N - 1, (K * (K - 1) / 2)] nn_dist_K;  //
  vector[P + 1] mu_beta;
  matrix[P + 1, P + 1] var_beta;
}
transformed data {
  cholesky_factor_cov[P + 1] d_var_beta;
  d_var_beta = cholesky_decompose(var_beta);
}
parameters {
  vector[P + 1] beta;
  real<lower = 0> sigma;
  real<lower = 0> tau;
  real<lower = 0> phi;
}
transformed parameters {
  real sigmasq = square(sigma);
  real tausq = square(tau);
  vector[N] y_hat = x * beta;
}
model {
  beta ~ multi_normal_cholesky(mu_beta, d_var_beta);
  phi ~ gamma(3, 0.5);
  sigma ~ normal(0, 1);
  tau ~ normal(0, 1);
  y ~ nngp(y_hat, sigmasq, tausq, phi, nn_dist, nn_dist_K, nn_ind, N, K);
}

