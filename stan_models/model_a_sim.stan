data {
  int<lower=1> N;
  int<lower=1> K;
  int<lower=0> N_disc;
  int<lower=1,upper=N_disc> disc[N];         // Discipline of the exam
  matrix[N, K] x;                            // Predictors
  vector[N] grade;                           // Outcome
}
parameters {
  real mu;
  vector[K] beta;
  vector[N_disc] alpha_disc; 
  real<lower=0> sigma_grade;
}
transformed parameters {
  vector[N] mu_grade;

  mu_grade = mu + alpha_disc[disc] + x * beta;
}
model {
  mu ~ std_normal();
  alpha_disc ~ normal(0, 0.5);
  sigma_grade ~ normal(0, 0.6);                
  beta ~ normal(0, 0.5);
  grade ~ normal(mu_grade, sigma_grade);
} 
generated quantities {
  real grade_pred[N];

  grade_pred = normal_rng(mu_grade, sigma_grade);
}

