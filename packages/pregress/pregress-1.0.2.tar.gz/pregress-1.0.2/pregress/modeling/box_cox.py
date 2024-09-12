import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import boxcox, boxcox_llf
import statsmodels.api as sm
import statsmodels.formula.api as smf

def box_cox(model):
    """
    Perform a Box-Cox transformation on the response variable of a given statsmodels regression results object,
    output a plot of the log-likelihood as a function of lambda, the fitted lambda, and the 95% confidence interval.

    Args:
        model (statsmodels.regression.linear_model.RegressionResultsWrapper): A fitted statsmodels regression model.
    """
    # Extract the response variable
    y = model.model.endog
    
    # Perform the Box-Cox transformation
    y_transformed, fitted_lambda = boxcox(y)
    
    # Calculate the log-likelihood for different lambda values using boxcox_llf
    lambdas = np.linspace(-2, 2, 100)
    log_likelihood = [boxcox_llf(lmbda, y) for lmbda in lambdas]
    
    # Calculate the 95% confidence interval
    max_log_likelihood = boxcox_llf(fitted_lambda, y)
    ci_cutoff = max_log_likelihood - 1.92  # Chi-squared distribution cutoff for 95% CI (1 degree of freedom)
    ci_lambdas = lambdas[np.array(log_likelihood) >= ci_cutoff]
    
    lambda_lower = ci_lambdas[0]
    lambda_upper = ci_lambdas[-1]
    
    # Plot the log-likelihood as a function of lambda
    plt.figure(figsize=(10, 6))
    plt.plot(lambdas, log_likelihood, label='Log-Likelihood')
    plt.axvline(fitted_lambda, color='r', linestyle='--', label=f'Fitted Lambda: {fitted_lambda:.4f}')
    plt.axvline(lambda_lower, color='b', linestyle='--', label=f'95% CI Lower: {lambda_lower:.4f}')
    plt.axvline(lambda_upper, color='b', linestyle='--', label=f'95% CI Upper: {lambda_upper:.4f}')
    plt.xlabel('Lambda')
    plt.ylabel('Log-Likelihood')
    plt.title('Box-Cox Transformation Log-Likelihood with 95% CI')
    plt.legend(loc='upper left')
    plt.grid(True)
    plt.show()
