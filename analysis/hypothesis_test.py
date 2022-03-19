
from statsmodels.graphics.gofplots import qqplot
from statsmodels.stats.stattools import jarque_bera
from scipy.stats import shapiro, normaltest
import numpy as np
from collections import defaultdict


def test_normality(data: np.ndarray) -> dict:
    '''
    Function to run normality tests on observed data
    :param data: an array containing observed random variable values. dtype: np.ndarray
    :return:
    results_dict: a dictionary containing different parameters of test keyed by respective test'strategy name
    '''
    assert isinstance(data, np.ndarray)
    # check if there are any nans
    num_nans = np.isnan(data).sum()
    if num_nans > 0:
        print(f"Data contains {num_nans} NaN values")
        print("Removing NaNs and running further tests")
        data = data[np.where(~np.isnan(data))[0]]
    results_dict = dict()
    # running jarque berra
    jb_results = jarque_bera(data)
    results_dict['jarque_berra'] = dict()
    results_dict['jarque_berra']['statistic'] = jb_results[0]
    results_dict['jarque_berra']['pvalue'] = jb_results[1]
    results_dict['jarque_berra']['skew'] = jb_results[2]
    results_dict['jarque_berra']['kurtosis'] = jb_results[3]
    # shapiro tests for normality
    shapiro_results = shapiro(data)
    results_dict['shapiro'] = dict()
    results_dict['shapiro']['statistic'] = shapiro_results[0]
    results_dict['shapiro']['pvalue'] = shapiro_results[1]
    # d_augostino tests for normality
    d_augostino_results = normaltest(data)
    results_dict['d_augostino'] = dict()
    results_dict['d_augostino']['statistic'] = d_augostino_results[0]
    results_dict['d_augostino']['pvalue'] = d_augostino_results[1]
    # ToDo: add more representative normality tests. For this, we need to study more on how to test normality
    return results_dict


def run_normality_test(data: np.ndarray, alpha=0.05):
    '''
    Runs all normality tests on the observed data and prints the results of running various normality tests
    :param data: an array containing observed random variable values. dtype: np.ndarray
    :param alpha: significance level for hypothesis testing
    :return: None
    '''
    assert isinstance(data, np.ndarray)
    results_dict = test_normality(data)
    results = defaultdict(lambda: [])
    results['test_name'].append('jarque_berra')
    results['statistic'].append(results_dict['jarque_berra']['statistic'])
    results['pvalue'].append(results_dict['jarque_berra']['pvalue'])
    print("Results from jarque berra tests:")
    print(f"Statistic: {results['statistic'][-1]:.2f}\np-value:"
          f"{results['pvalue'][-1]:.2f} skewness: {results_dict['jarque_berra']['skew']:.2f}\n"
          f"kurtosis: {results_dict['jarque_berra']['kurtosis']:.2f}")
    results['test_extra_statistics'].append(f"skewness: {results_dict['jarque_berra']['skew']}\n kurtosis: {results_dict['jarque_berra']['kurtosis']}")
    if results_dict['jarque_berra']['pvalue'] < alpha:
        results['RejectHypothesis'].append(True)
        print(f"Jarque berra rejects the Hypothesis of Gaussian(p:{results_dict['jarque_berra']['pvalue']:.2f})")
    else:
        results['RejectHypothesis'].append(False)
        print(
            f"Jarque berra fails to reject the Hypothesis of Gaussian(p:{results_dict['jarque_berra']['pvalue']:.2f})")
    print("#" * 20)
    print("Results from shapiro tests:")
    results['test_name'].append('shapiro')
    results['statistic'].append(results_dict['shapiro']['statistic'])
    results['pvalue'].append(results_dict['shapiro']['pvalue'])
    results['test_extra_statistics'].append('NA')
    print(f"Statistic: {results_dict['shapiro']['statistic']:.2f}\np-value:"
          f"{results_dict['shapiro']['pvalue']:.2f}")
    if results_dict['shapiro']['pvalue'] < alpha:
        results['RejectHypothesis'].append(True)
        print(f"Shapiro rejects the Hypothesis of Gaussian(p:{results_dict['shapiro']['pvalue']:.2f})")
    else:
        results['RejectHypothesis'].append(False)
        print(f"Shapiro fails to reject the Hypothesis of Gaussian(p:{results_dict['shapiro']['pvalue']:.2f})")
    print("#" * 20)
    print("Results from D`Augostino'strategy K^2 tests:")
    results['test_name'].append("D`Augostino'strategy K^2")
    results['statistic'].append(results_dict["d_augostino"]['statistic'])
    results['pvalue'].append(results_dict["d_augostino"]['pvalue'])
    results['test_extra_statistics'].append("NA")
    print(f"Statistic: {results_dict['d_augostino']['statistic']:.2f}\np-value:"
          f"{results_dict['d_augostino']['pvalue']:.2f}")
    if results_dict['d_augostino']['pvalue'] < alpha:
        results['RejectHypothesis'].append(True)
        print(f"Shapiro rejects the Hypothesis of Gaussian(p:{results_dict['d_augostino']['pvalue']:.2f})")
    else:
        results['RejectHypothesis'].append(False)
        print(f"Shapiro fails to reject the Hypothesis of Gaussian(p:{results_dict['d_augostino']['pvalue']:.2f})")
    results_df = pd.DataFrame(results)
    return results_df
