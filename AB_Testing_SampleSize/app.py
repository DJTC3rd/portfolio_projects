import numpy as np
import streamlit as st
from skopt import gp_minimize

from SampleSizeCalculations.freqseq.calibration import build_test, objective_function
from SampleSizeCalculations.basic_power_test import ttest_sample_size

@st.cache_data
def get_sequential_test_results(p, delta, alpha, beta):
    """Caches test constrains for use in app"""
    N, d, sigma, fpr, tpr = build_test(p, delta, alpha, beta, 5000)
    initial_error = np.abs(tpr - beta) + np.abs(fpr - alpha)

    if initial_error <= 0.04:
        return N, d, sigma, fpr, tpr

    def error_function(x):
        return objective_function(p, delta, alpha, beta, x[0], x[1])

    alpha_min = alpha / 40
    alpha_max = min(1, 6 * alpha)
    beta_min = beta - beta / 8
    beta_max = min(1, beta + beta / 8)

    res = gp_minimize(
        error_function,
        [(alpha_min, alpha_max), (beta_min, beta_max)],
        x0=[alpha, beta],
        n_calls=20,
        random_state=777,
        verbose=True,
    )

    best_alpha = res.x[0]
    best_beta = res.x[1]

    return build_test(p, delta, best_alpha, best_beta)


@st.cache_data
def get_fixed_test_results(baseline, alpha, beta, delta, relative):
    return ttest_sample_size(baseline, alpha, beta, delta, relative)

st.write(
    """
    # A\B Testing Sample Size Calculator.

    This calculator yields sample size requirements for a sequential test or a standard fixed test. 
   
    """
)

tab1, tab2 = st.tabs(['Standard','Sequential'])

with tab1:
    st.write('''## Test Parameters''')
    effect_type = st.checkbox('Relative Effect', value=True)

    baseline_rate = st.number_input(
        "Baseline Observation",
        min_value=0.01,
        max_value=0.95,
        value=0.2,
    )

    delta_fixed = st.number_input(
        "Insert the minimum detectable effect",
        min_value=-0.9,
        max_value=0.9,
        step=0.05,
        value=0.05,
    )
    if delta_fixed == 0:
        raise ValueError(f"Delta cannot be equal to zero!")

    alpha_fixed = st.number_input(
        "Desired significance level (alpha)", min_value=0.0, max_value=1.0, value=0.05, key='alpha_fixed'
    )

    beta_fixed = st.number_input(
        "Desired Statistical Power (beta)", min_value=0.0, max_value=1.0, value=0.8, key='beta_fixed'
    )

    daily_conversions_fixed = st.number_input(
        "Approximate number of daily conversions", min_value=0, value=100, key = 'fixed_daily'
    )

    N = get_fixed_test_results(baseline_rate, alpha_fixed, beta_fixed, delta_fixed, effect_type)

    st.markdown(f"#### The potential runtime is {np.ceil(N/daily_conversions_fixed)} day(s).")

    st.metric("The test requires each group have:", int(N))

with tab2:
    st.write('''## Test Parameters''')
    two_sided = st.checkbox('Two sided experiment')
    # this is the probability of being assigned to the treatment group (i.e.  for Control/Treatment: 50 in 50/50, or 40  in 60/40)
    p = st.number_input(
        "Percentage of test users assigned treatment",
        min_value=0.01,
        max_value=0.95,
        value=0.5,
    )

    delta = st.number_input(
        "Insert the minimum detectable effect",
        min_value=-0.9,
        max_value=0.9,
        step=0.05,
        value=0.3,
    )
    if delta == 0:
        raise ValueError(f"Delta cannot be equal to zero!")

    alpha = st.number_input(
        "Desired significance level (alpha)", min_value=0.0, max_value=1.0, value=0.05,key='alpha_seq'
    )

    beta = st.number_input(
        "Desired Statistical Power (beta)", min_value=0.0, max_value=1.0, value=0.8,key='beta_seq'
    )

    daily_conversions = st.number_input(
        "Approximate number of daily conversions", min_value=0, value=100, key='beta_daily'
    )

    if two_sided:
        alpha = alpha/2
    
    N, d, sigma, fpr, tpr = get_sequential_test_results(p, delta, alpha, beta)

    if two_sided:
        fpr = fpr*2
    
    st.write(
        """
    ### Test Specifications

    Note that this app verifies the validity of the test by running simulations and presenting
    the empirical true and false positive rates. 
    """
    )
    st.markdown(f"#### The maximum potential runtime is {np.ceil(N/daily_conversions)} day(s).")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Conversions", int(N),help='Control wins if this many samples is obtained.')
    col2.metric("Treatment Conversions Lead", int(d), help='Treatment wins if group is ahead of control by this value.')
    col3.metric("Drift (σ)", np.round(sigma, 3), help='This value accounts for a drift based on treatment  group allocataion. A value of 1 is neutral.')
    col1.metric("Simulated Alpha Value", np.round(fpr, 2), help='The simulated alpha value.')
    col2.metric("Simulated Statistical Power", np.round(tpr, 2), help='The simulated statistical power.')


    st.write (
        '''
        ## Analyze Results
          Use this form to analyze the results of the above test.
          If returning to this page make sure that the above values are set for the test.  
    '''
    )

    control_conversions = st.number_input("Control Group Conversions", min_value=0.0)
    treatment_conversions = st.number_input("Treatment Group Conversions", min_value=0.0)

    if st.button('Get Results'):
        if delta > 0:
            value = (treatment_conversions - control_conversions 
                       - (treatment_conversions + control_conversions)*(2*p - 1))/sigma
            if (int(value) > int(d)) and (treatment_conversions + control_conversions < int(N)):
                st.write('The treatment performed better than the control')
            elif (int(value) < int(d)) and (treatment_conversions + control_conversions >= int(N)):
                st.write('There is no winner')
            else:
                st.write('Consult with the data team.')
        elif delta < 0:
            value = (control_conversions - treatment_conversions
                       - (treatment_conversions + control_conversions)*(2*(1-p) - 1))/sigma
            if (int(value) > int(d)) and (treatment_conversions + control_conversions < int(N)):
                st.write('The treatment performed better than the control')
            elif (int(value) < int(d)) and (treatment_conversions + control_conversions >= int(N)):
                st.write('There is no winner')
            else:
                st.write('Consult with the data team.')
