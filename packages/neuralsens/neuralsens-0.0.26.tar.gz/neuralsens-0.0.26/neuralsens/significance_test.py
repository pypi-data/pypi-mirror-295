import numpy as np
from scipy.optimize import brentq
import pandas as pd
from sklearn.utils import resample


def ecdf(data):
    """
    Create an empirical cumulative distribution function (ECDF) for a given set of data.

    Parameters:
    data (array): Array of data points.

    Returns:
    function: A function that calculates the ECDF for a given value x.
    """
    sorted_data = np.sort(data)
    n = len(data)

    def ecdf_func(x):
        return np.searchsorted(sorted_data, x, side="right") / n

    return ecdf_func


def find_critical_value(data, alpha):
    """
    Find the critical value for a given set of data and alpha.

    Parameters:
    data (array): Array of data points.
    alpha (float): Significance level.

    Returns:
    float: The critical value such that P(X <= x) >= 1 - alpha.
    """
    ecdf_func = ecdf(data)
    lower_bound = min(data)
    upper_bound = max(data)

    def func_to_root(x):
        return ecdf_func(x) - (1 - alpha)

    critical_value = brentq(func_to_root, lower_bound, upper_bound)
    return critical_value


def k_step_m_algorithm(original_stats, bootstrap_stats, num_hypotheses, alpha, k):
    """
    Implement the k-stepM algorithm for multiple hypothesis testing.

    Parameters:
    original_stats (array): Array of original test statistics for each hypothesis.
    bootstrap_stats (matrix): Matrix of bootstrap test statistics (rows: bootstrap samples, columns: hypotheses).
    num_hypotheses (int): Total number of hypotheses.
    alpha (float): Significance level.
    k (int): Threshold number for controlling the k-familywise error rate.

    Returns:
    dict: Contains 'signif' (indicating which hypotheses are rejected) and 'cv' (critical values).
    """
    ordered_indices = np.argsort(original_stats)[::-1]  # Descending order
    ordered_tnj = original_stats[ordered_indices]
    ordered_tnj_b = bootstrap_stats[:, ordered_indices]

    # Initialize critical values
    c_kv = np.zeros(num_hypotheses)

    # Configuration
    B = bootstrap_stats.shape[0]

    while np.sum(c_kv == 0) >= 1:
        K = c_kv[ordered_indices] == 0
        kmax_nk_b = []

        for b in range(B):
            differences = ordered_tnj_b[b, K] - ordered_tnj[K]
            sorted_differences = np.sort(differences)[::-1]
            kmax_nk_b.append(sorted_differences[:k].max())

        kmax_nk_b = np.array(kmax_nk_b)

        if len(np.unique(kmax_nk_b)) > 2:
            c_K = abs(find_critical_value(kmax_nk_b, alpha))
        else:
            c_K = abs(kmax_nk_b.max())

        R1 = np.sum((original_stats[c_kv == 0] - c_K) > 0)
        if R1 < k:
            break

        c_kv[(c_kv == 0) & ((original_stats - c_K) > 0)] = c_K

    c_kv[c_kv == 0] = c_K

    return {"signif": (original_stats - c_K) > 0, "cv": c_kv, "alpha": alpha}


def significance_mlp(
    X, y, train_mlp_func, calculate_derivatives_func, num_bootstrap=100, alpha=0.05
):
    """
    Test the significance of the inputs of an MLP model using a user-defined training function.

    Parameters:
    X (DataFrame): Features of the original dataset used for MLP training.
    y (Series or DataFrame): Target variable of the original dataset.
    train_mlp_func (function): User-defined function to train the MLP model.
    calculate_derivatives_func (function): Function to calculate derivatives from the Jacobian_MLP object.
    num_bootstrap (int): Number of bootstrap iterations. Defaults to 100.
    alpha (float): Significance level for k-step M algorithm. Defaults to 0.05.

    Returns:
    dict: Results from the kStepMAlgorithm.
    """

    # Combine X and y for bootstrapping
    original_data = pd.concat([X, y], axis=1)

    # Step 1: Train MLP with original data and calculate derivatives
    original_model = train_mlp_func(X, y)
    original_sens = calculate_derivatives_func(original_model, X, y)
    original_measures = original_sens.sens[0]

    # Step 2: Bootstrapping and training
    bootstrapped_measures = np.zeros(original_measures.shape + (num_bootstrap,))
    bootstrapped_derivatives = np.zeros(
        original_sens.raw_sens[0].shape + (num_bootstrap,)
    )

    for i in range(num_bootstrap):
        # Bootstrap the dataset
        bootstrapped_data = resample(original_data)

        # Separate the bootstrapped data into features and target
        X_boot, y_boot = (
            bootstrapped_data.drop(y.columns, axis=1),
            bootstrapped_data[y.columns],
        )

        # Train MLP model on bootstrapped data
        bootstrapped_model = train_mlp_func(X_boot, y_boot)

        # Calculate derivatives
        bootstrapped_sensmlp = calculate_derivatives_func(
            bootstrapped_model, X_boot, y_boot
        )

        bootstrapped_measures[:, :, i] = bootstrapped_sensmlp.sens[0].values
        bootstrapped_derivatives[:, :, i] = bootstrapped_sensmlp.raw_sens[0].values

    # Step 3: Apply kStepMAlgorithm
    num_hypotheses = bootstrapped_measures.shape[0]
    results = []
    for i in (1, 2):
        results.append(
            k_step_m_algorithm(
                original_measures.iloc[:, i],
                bootstrapped_measures[:, i, :],
                num_hypotheses,
                alpha,
                1,
            )
        )

    return results
