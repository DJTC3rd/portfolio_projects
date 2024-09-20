import scipy.stats
import numpy as np
# Test Case gives 1030 as evan miller calculator for absolute
# p = 0.2
# alpha = 0.05
# power_level = 0.8 
# delta = 0.05

def ttest_sample_size(baseline_rate, alpha, statistical_power, mde, relative):
    if( baseline_rate >0.5):
        baseline_rate = 1 - baseline_rate
    
    if relative:
        mde = baseline_rate*mde

    t_alpha2 = scipy.stats.norm.ppf(1 - alpha/2)
    t_beta = scipy.stats.norm.ppf(statistical_power)

    sd1 = np.sqrt(2*baseline_rate*(1 - baseline_rate))
    sd2 = np.sqrt(baseline_rate * (1 - baseline_rate) + (baseline_rate + mde)*(1 - baseline_rate - mde))

    return round((t_alpha2 * sd1 + t_beta * sd2) * (t_alpha2 * sd1 + t_beta * sd2) / (mde * mde))

def get_random_t_result(sample_size, effect_size):
    """
    perform a ttest on random data of n=sampSize
    """
    group1 = np.random.normal(loc=0.0, scale=1.0, size=sample_size)
    group2 = np.random.normal(loc=effect_size, scale=1.0, size=sample_size)
    ttresult = scipy.stats.ttest_ind(group1, group2)
    return(ttresult.pvalue)


def simulate_power(sample_size, effect_size):
    pvals = np.empty(5000)
    for i in range(5000):
        pvals[i] = get_random_t_result(sample_size, effect_size) < 0.05
    print(len(pvals))
    print(np.sum(pvals))
    return np.mean(pvals)
