import gpmp.num as gnp
import gpmp as gp
import scipy.stats as stats

def predict_with_bayesian_confidence_intervals(model, xi, zi, xt, alpha=0.05):
    """
    Compute Bayesian confidence intervals from posterior mean and variance.

    Parameters
    ----------
    zpm : array_like
        Posterior mean, 1D array of shape (n,).
    zpv : array_like
        Posterior variance, 1D array of shape (n,).
    alpha : float, optional
        Significance level for the confidence interval (default is 0.05).

    Returns
    -------
    lower_bounds : array-like
        Lower bounds of the confidence intervals.
    upper_bounds : array_like
        Upper bounds of the confidence intervals.
    """

    zpm, zpv = model.predict(xi, zi, xt)
        
    z_score = stats.norm.ppf(1 - alpha / 2)

    std_dev = gnp.sqrt(zpv)

    lower_bounds = zpm - z_score * std_dev
    upper_bounds = zpm + z_score * std_dev

    return zpm, zpv, lower_bounds, upper_bounds

def predict_with_jacknife_confidence_intervals(model, xi, zi, xt, alpha=0.05):
    
