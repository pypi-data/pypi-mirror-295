# TwoSampleHC -- Higher Criticism Test between Two Frequency Tables

This package provides an adaptation of the Donoho-Jin-Tukey Higher-
Critisim (HC) test to frequency tables. This adapatation uses a binomial
allocation model for the number of occurances of each feature in two-
samples, each of which is associated with a frequency table. The exact
binomial test associated with each feature yields a p-value. The HC
statistic combines these P-values to a global test against the null
hypothesis that the two tables are two realizations of the same data
generating mechanism. 

This test is particularly useful in identifying non-null effects under
weak and sparse alternatives, i.e., when the difference between the
tables is due to few features, and the evidence each such feature
provide is realtively weak. See references below for more details.
[1] Alon Kipnis. (2022). Higher Criticism for Discriminating Word
 Frequency Tables and Testing Authorship. Annals of Applied Statistics.
[2] David L. Donoho and Alon Kipnis. (2022). Higher criticism to compare
 two large frequency tables, with sensitivity to possible rare and weak
 differences. Annals of Statistics. 


## Example:
```
from TwoSampleHC import two_sample_pvals, HC
import numpy as np

N = 1000 # number of features
n = 5 * N #number of samples

P = 1 / np.arange(1,N+1) # Zipf base distribution
P = P / P.sum()

ep = 0.02 #fraction of features to perturb
mu = 0.005 #intensity of perturbation

TH = np.random.rand(N) < ep
Q = P.copy()
Q[TH] += mu
Q = Q / np.sum(Q)

smp_P = np.random.multinomial(n, P)  # sample form P
smp_Q = np.random.multinomial(n, Q)  # sample from Q

pv = two_sample_pvals(smp_Q, smp_P) # binomial P-values
hc = HC(pv)
hc_val, p_th = hc.HCstar(gamma = 0.25) # Small sample Higher Criticism test

print("TV distance between P and Q: ", 0.5*np.sum(np.abs(P-Q)))
print("Higher-Criticism score for testing P == Q: ", hc_val)  
```
