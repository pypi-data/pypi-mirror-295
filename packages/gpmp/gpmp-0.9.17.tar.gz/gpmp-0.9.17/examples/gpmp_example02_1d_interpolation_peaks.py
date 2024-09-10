"""
Plot and optimize the restricted negative log-likelihood

Author: Emmanuel Vazquez <emmanuel.vazquez@centralesupelec.fr>
Copyright (c) 2022-2023, CentraleSupelec
License: GPLv3 (see LICENSE)
"""

import gpmp.num as gnp
import gpmp as gp
import matplotlib.pyplot as plt


def f_matern(x):
    l = 0.1  # length scale
    x1, x2, x3, x4 = -0.5, -0.2, 0.3, 0.5  # translation points
    x = gnp.asarray(x)
    return gnp.exp(-1.0 + 0.2 * x**2 - 
        0.1 * gp.kernel.matern32_kernel(gnp.abs(x - x1) / 0.01)
        - 0.2 * gp.kernel.matern32_kernel(gnp.abs(x - x2) / 0.02)
        - 0.1 * gp.kernel.matern32_kernel(gnp.abs(x - x3) / 0.04)
        - 0.2 * gp.kernel.matern32_kernel(gnp.abs(x - x4) / 0.04)
    )


def generate_data():
    """
    Data generation.

    Returns
    -------
    tuple
        (xt, zt): target data
        (xi, zi): input dataset
    """
    dim = 1
    nt = 1000
    box = [[-1], [1]]
    xt = gp.misc.designs.regulargrid(dim, nt, box)
    zt = f_matern(xt)

    ni = 40
    xi = gp.misc.designs.ldrandunif(dim, ni, box)
    zi = f_matern(xi)

    return xt, zt, xi, zi


def constant_mean(x, param):
    return gnp.ones((x.shape[0], 1))


def kernel(x, y, covparam, pairwise=False):
    p = 1
    return gp.kernel.maternp_covariance(x, y, p, covparam, pairwise)


def visualize_results(xt, zt, xi, zi, zpm, zpv):
    """
    Visualize the results using gp.misc.plotutils (a matplotlib wrapper).

    Parameters
    ----------
    xt : numpy.ndarray
        Target x values
    zt : numpy.ndarray
        Target z values
    xi : numpy.ndarray
        Input x values
    zi : numpy.ndarray
        Input z values
    zpm : numpy.ndarray
        Posterior mean
    zpv : numpy.ndarray
        Posterior variance
    """
    fig = gp.misc.plotutils.Figure(isinteractive=True)
    fig.plot(xt, zt, "k", linewidth=1, linestyle=(0, (5, 5)))
    fig.plotdata(xi, zi)
    fig.plotgp(xt, zpm, zpv, colorscheme="simple")
    fig.xylabels("$x$", "$z$")
    fig.title("Posterior GP with parameters selected by ReML")
    fig.show(grid=True, xlim=[-1.0, 1.0], legend=True, legend_fontsize=9)


def main():
    xt, zt, xi, zi = generate_data()

    model = gp.core.Model(constant_mean, kernel)

    # Automatic selection of parameters using REML
    model, info = gp.kernel.select_parameters_with_remap(model, xi, zi, info=True)
    gp.misc.modeldiagnosis.diag(model, info, xi, zi)

    # Prediction
    zpm, zpv = model.predict(xi, zi, xt)

    # Visualization
    print("\nVisualization")
    print("-------------")
    plot_likelihood = False
    if plot_likelihood:
        gp.misc.modeldiagnosis.plot_likelihood_sigma_rho(model, info)

    visualize_results(xt, zt, xi, zi, zpm, zpv)

    zloo, sigma2loo, eloo = model.loo(xi, zi)

    plt.figure()
    plt.plot(zi, eloo / sigma2loo, 'o')
    plt.show()

    r = gnp.to_np(eloo / sigma2loo)
    
    from scipy.stats import gennorm
    import numpy as np
    
    shape, loc, scale = gennorm.fit(r)
    print(f"Shape (beta): {shape}")
    print(f"Location (mu): {loc}")
    print(f"Scale (alpha): {scale}")

    # Plot the histogram of the data
    plt.figure()
    plt.hist(r, bins=30, density=True, alpha=0.6, color='g')

    # Create a range of values for the PDF
    xmin, xmax = plt.xlim()
    x_range = np.linspace(xmin, xmax, 100)

    # Plot the fitted PDF
    pdf_fitted = gennorm.pdf(x_range, shape, loc, scale)
    plt.plot(x_range, pdf_fitted, 'k', linewidth=2)

    # Display the plot
    plt.title('Fit of Generalized Gaussian Distribution')
    plt.xlabel('Data')
    plt.ylabel('Density')
    plt.show()


if __name__ == "__main__":
    main()
