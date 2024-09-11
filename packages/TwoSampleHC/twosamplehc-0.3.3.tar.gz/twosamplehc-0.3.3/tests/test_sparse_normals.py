import sys
sys.path.append("../src")
from TwoSampleHC import HigherCriticism
import numpy as np
from tqdm import tqdm
from scipy.stats import norm

"""
Here we create two multivariate normals with rare
and weak differences in their means. 
"""

GAMMA = .3

def test_sparse_normals(r, n, be, sig):
    mu = np.sqrt(2 * r * np.log(n))
    ep = n ** -be
    idcs1 = np.random.rand(n) < ep / 2
    idcs2 = np.random.rand(n) < ep / 2

    Z1 = np.random.randn(n)
    Z2 = np.random.randn(n)

    Z1[idcs1] = sig*Z1[idcs1] + mu
    Z2[idcs2] = sig*Z2[idcs2] + mu

    Z = (Z1 - Z2)/np.sqrt(2)
    pvals = 2*norm.cdf(- np.abs(Z))

    _hc = HigherCriticism(pvals)

    return {'hc' : _hc.HC(GAMMA)[0],
            'hcstar' : _hc.HCstar(GAMMA)[0],
            }
    

n = 1000
be = .75
sig = 1

nMonte = 10000


lo_res = {}
for key in ['hc', 'hcstar']:
    lo_res[key] = []
r = 0
print(f"Testing with parameters: r={r}, n={n}, be={be}, sig={sig}")
for itr in tqdm(range(nMonte)):
    res = test_sparse_normals(r, n, be, sig)
    for key in res:
        lo_res[key]+=[res[key]]
    
print("Avg(HC) = ", np.mean(lo_res['hc']))
print("Avg(HCstar) = ", np.mean(lo_res['hcstar']))

assert(np.abs(np.mean(lo_res['hc']) - 1.33) < .15)
assert(np.abs(np.mean(lo_res['hcstar']) - 1.29) < .15)

lo_res = {}
for key in ['hc', 'hcstar']:
    lo_res[key] = []
r = .75
print(f"Testing with parameters: r={r}, n={n}, be={be}, sig={sig}")
for itr in tqdm(range(nMonte)):
    res = test_sparse_normals(r, n, be, sig)
    for key in res:
        lo_res[key]+=[res[key]]
    

print("Avg(HC) = ", np.mean(lo_res['hc']))
print("Avg(HCstar) = ", np.mean(lo_res['hcstar']))

assert(np.abs(np.mean(lo_res['hc']) - 1.72) < .15)
assert(np.abs(np.mean(lo_res['hcstar']) - 1.69) < .15)


r = .75
be = .9
lo_res = {}
for key in ['hc', 'hcstar', 'bj', 'bonf', 'fdr']:
    lo_res[key] = []

print(f"Testing with parameters: r={r}, n={n}, be={be}, sig={sig}")
for itr in tqdm(range(nMonte)):
    res = test_sparse_normals(r, n, be, sig)
    for key in res:
        lo_res[key]+=[res[key]]
    

print("Avg(HC) = ", np.mean(lo_res['hc']))
print("Avg(HCstar) = ", np.mean(lo_res['hcstar']))

assert(np.abs(np.mean(lo_res['hc']) - 1.48) < .15)
assert(np.abs(np.mean(lo_res['hcstar']) - 1.44) < .15)
