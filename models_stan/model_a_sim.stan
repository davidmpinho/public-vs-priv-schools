data {
  int<lower=1> N;
  int<lower=1> P;
  int<lower=0> N_county;
  int<lower=0> N_school;
  int<lower=1,upper=N_county> county[N];     // County of the school
  int<lower=1,upper=N_school> school[N];     // School
  matrix[N, P] x;                            // Predictors
  vector[N] grade;                           // Outcome
}
parameters {
  real mu;
  vector[P] beta;
  vector[N_county] alpha_county;
  vector[N_school] alpha_school;
  real<lower=0> sigma_county;
  real<lower=0> sigma_school;
  real<lower=0> sigma_grade;
}
transformed parameters {
  vector[N] mu_grade;

  mu_grade = (mu
                + alpha_county[county] * sigma_county
                + alpha_school[school] * sigma_school
                + x * beta);
}
model {
  mu ~ std_normal();
  alpha_county ~ normal(0, 0.5);
  alpha_school ~ normal(0, 0.5);
  sigma_county ~ normal(0, 0.5);
  sigma_school ~ normal(0, 0.5);
  sigma_grade ~ normal(0, 0.6);
  beta ~ normal(0, 0.5);
  grade ~ normal(mu_grade, sigma_grade);
} 
generated quantities {
  real grade_rng[N];

  grade_rng = normal_rng(mu_grade, sigma_grade);
}

