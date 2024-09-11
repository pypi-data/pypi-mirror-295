
def hc_vals(pv, gamma=0.2, minPv='one_over_n', stbl=True):
    """
    Evalaute Higher Criticism of a list of P-values. 
    
    Higher Criticism test 

    Args:
    -----
        pv : list of p-values. P-values that are np.nan are exluded.
        gamma : lower fruction of p-values to use.
        stbl : use expected p-value ordering (stbl=True) or observed 
                (stbl=False)
        minPv : integer or string 'one_over_n' (default).
                 Ignote smallest minPv-1 when computing HC score.

    Return :
    -------
        hc_star : sample adapted HC (HC dagger in [1])
        p_star : HC threshold: upper boundary for collection of
                 p-value indicating the largest deviation from the
                 uniform distribution.

    """
    EPS = 0.01/len(pv)
    pv = np.asarray(pv).copy()
    n = len(pv)  #number of features
    
    #n = len(pv)
    hc_star = np.nan
    p_star = np.nan

    if n > 1:
        ps_idx = np.argsort(pv)
        ps = pv[ps_idx]  #sorted pvals

        uu = np.linspace(1 / n, 1-EPS, n)  #expectation of p-values under
        # H0; largest P-value assumed to have not effect. 
        i_lim_up = np.maximum(int(np.floor(gamma * n + 0.5)), 1)

        ps = ps[:i_lim_up]
        uu = uu[:i_lim_up]
        
        if minPv == 'one_over_n' :
            i_lim_low = np.argmax(ps > (1-EPS)/n)
        else :
            i_lim_low = minPv

        if stbl:
            z = (uu - ps) / np.sqrt(uu * (1 - uu)) * np.sqrt(n)
        else:
            z = (uu - ps) / np.sqrt(ps * (1 - ps)) * np.sqrt(n)

        i_lim_up = max(i_lim_low + 1, i_lim_up)

        i_max_star = np.argmax(z[i_lim_low:i_lim_up]) + i_lim_low

        z_max_star = z[i_max_star]

        hc_star = z[i_max_star]
        p_star = ps[i_max_star]

    return hc_star, p_star
