import numpy as np
from numpy import pi, sin, cos, exp, log, sqrt
from scipy.optimize import newton
import astropy.constants as ac

from enterprise.signals.signal_base import function as enterprise_function
from enterprise.signals.deterministic_signals import Deterministic
from enterprise.signals.parameter import Uniform

# from custom_priors import CircularUniform # this is actually not needed since the auxiliary jump is executed before the log_prior evaluation

GMsun = ac.GM_sun.value  # [m^3/s^2]
AU = ac.au.value  # [m]
clight = ac.c.value  # [m/s^2]
day2s = 86400  # [s]
pi = np.pi


@enterprise_function
def troj_res(toas, n_b, log_B, nu, theta, phi, T_asc):
    """
    Calculate the timing perturbation due to an object passing a pulsar
    on a hyperbolic orbit.

    Inputs
    ------
    toas  : TOAs of the pulsar [s]
    n_b  : binary orbital frequency [rad s^-1]
    log_B : log10 of libration amplitude [lts]
    nu   : libration frequency [rad s^-1]
    phi_plus  : arbitrary phase for the n_b + nu frequency term
    phi_minus  : arbitrary phase for the n_b - nu frequency term


    Outputs
    -------
    Rs : array-like
        Induced timing residuals (s) evaluated at TOAs.
    """
    t = toas - T_asc
    B = 10**log_B
    #     n_b = n_b.value
    n_b_t = n_b * t
    nu_t = nu * t

    trojan_residuals = B * (
        np.cos(n_b_t + theta) * np.cos(nu_t + phi)
        + 2 / 3 * nu / n_b * np.cos(n_b_t + theta - pi / 2) * np.sin(nu_t + phi)
    )

    parabolic_fit = np.polyval(np.polyfit(t, trojan_residuals, 2), t)
    trojan_residuals -= parabolic_fit
    # subtracts the parabolic fit from the trojan residuals

    return trojan_residuals


def troj_res_block(
    nu,
    n_b,
    T_asc,
    log_B=Uniform(-12, -4),
    theta=Uniform(pi / 3, 2 * pi / 3),
    phi=Uniform(0, 2 * pi),
    name="troj",
):

    return Deterministic(
        troj_res(log_B=log_B, nu=nu, theta=theta, phi=phi, n_b=n_b, T_asc=T_asc),
        name=name,
    )
