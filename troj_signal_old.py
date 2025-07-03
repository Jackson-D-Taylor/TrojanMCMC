
import numpy as np
from numpy import pi, sin, cos, exp, log, sqrt
from scipy.optimize import newton
import astropy.constants as ac

from enterprise.signals.signal_base import function as enterprise_function
from enterprise.signals.deterministic_signals import Deterministic
from enterprise.signals.parameter import Uniform

GMsun = ac.GM_sun.value #[m^3/s^2]
AU = ac.au.value #[m]
clight = ac.c.value #[m/s^2]
day2s = 86400 #[s]


# def v_from_beM(b, e, M=1.4):
#     """
#     b: impact parameter [m]
#     e: eccentricity
#     M: total mass [Msun]
#     """
#     vinf = np.sqrt(GMsun * M/b) * (e**2 -1)**(1/4)
    
#     return vinf


# def H_from_t_ross(t, e, niter=5):
#     '''
#     Calculate the hyperbolic anomaly `H` (dimensionless) 
#     given a time `t` in units of b/v_0.
#     '''
#     H = np.arcsinh(np.cbrt(6*np.sqrt(e**2-1)/e*t)+np.sqrt(e**2-1)/e*t)
#     for i in range(niter):
#         H = H - (e*np.sinh(H) - H - t*np.sqrt(e**2-1))/(e*np.cosh(H)-1)
#     return H


# # def H_from_t_ross_old(t, e):
# #     '''
# #     Calculate the hyperbolic anomaly `H` (dimensionless) 
# #     given a time `t` in units of b/v_0.
# #     '''
# #     def t_from_H(H):
# #         return (e*np.sinh(H)-H)/np.sqrt(e**2-1)
    
# #     try:
# #         H = [newton(lambda H: t_from_H(H)-t, np.arcsinh(np.cbrt(6*np.sqrt(e**2-1)/e*t)+np.sqrt(e**2-1)/e*t)) for t in t]
# #         H = np.array(H)
# #     except TypeError:
# #         H = newton(lambda H: t_from_H(H)-t, np.arcsinh(np.cbrt(6*np.sqrt(e**2-1)/e*t)+np.sqrt(e**2-1)/e*t))
# #     return H


# def H_from_t_mikkola(t, e):
#     l = t * np.sqrt(e*e - 1)
    
#     alpha = (e-1)/(4*e + 0.5)
#     alpha3 = alpha*alpha*alpha
#     beta = (l/2)/(4*e + 0.5)
#     beta2 = beta*beta;

#     z = np.cbrt(beta + np.sqrt(alpha3 + beta2))
    
#     s = (z - alpha/z)
#     s5 = s*s*s*s*s

#     ds = 0.071*s5/((1+0.45*s*s)*(1+4*s*s)*e)
#     w = s+ds

#     u = 3*np.log(w+np.sqrt(1+w*w))

#     esu= e*np.sinh(u)
#     ecu= e*np.cosh(u)

#     fu  = -u + esu - l
#     f1u = -1 + ecu  
#     f2u = esu
#     f3u = ecu
#     f4u = esu
#     f5u = ecu

#     u1 = -fu/ f1u
#     u2 = -fu/(f1u + f2u*u1/2)
#     u3 = -fu/(f1u + f2u*u2/2 + f3u*(u2*u2)/6.0)
#     u4 = -fu/(f1u + f2u*u3/2 + f3u*(u3*u3)/6.0 + f4u*(u3*u3*u3)/24.0)
#     u5 = -fu/(f1u + f2u*u4/2 + f3u*(u4*u4)/6.0 + f4u*(u4*u4*u4)/24.0 + f5u*(u4*u4*u4*u4)/120.0)
#     uM = (u + u5)
    
#     return uM


@enterprise_function
def troj_res(toas, n_b, log_B, nu, phi_plus, phi_minus):
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
    t = toas
    B = 10**log_B
#     n_b = n_b.value


    trojan_residuals = B * (np.cos((n_b+nu)*t + phi_plus) + np.cos((n_b - nu)*t + phi_minus))
    
    return trojan_residuals

@enterprise_function
def troj_res_2nd(toas, n_b, log_D, nu, theta, phi):
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
    t = toas
    D = 10**log_D
#     n_b = n_b.value


    trojan_residuals = D * np.cos(n*t + theta) * np.cos(nu*t + phi)
    
    return trojan_residuals

@enterprise_function
def troj_res_unif(toas, n_b, B, nu, phi_plus, phi_minus):
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
    t = toas
    trojan_residuals = B * (np.cos((n_b+nu)*t + phi_plus) + np.cos((n_b - nu)*t + phi_minus))
    
    return trojan_residuals


def troj_res_block(
    nu,
    n_b,
    log_B = Uniform(-9, -5),
    phi_plus = Uniform(-20*np.pi, 20*np.pi),
    phi_minus = Uniform(-20*np.pi, 20*np.pi),
    name = "troj",
    ):
    
    return Deterministic(
        troj_res(log_B=log_B,
                nu = nu,
                phi_plus = phi_plus,
                phi_minus = phi_minus,
                n_b = n_b
               ),
        name = name,
    )

def troj_res_block_2nd(
    nu,
    n_b,
    log_D = Uniform(-9, -5),
    theta = Uniform(-20*np.pi, 20*np.pi),
    phi = Uniform(-20*np.pi, 20*np.pi),
    name = "troj",
    ):
    
    return Deterministic(
        troj_res(log_D=log_D,
                nu = nu,
                theta = theta,
                phi = phi,
                n_b = n_b
               ),
        name = name,
    )

def troj_res_block_unif(
    nu,
    n_b,
    B, # need to define B prior outside of here
    phi_plus = Uniform(-20*np.pi, 20*np.pi),
    phi_minus = Uniform(-20*np.pi, 20*np.pi),
    name = "troj",
    ):
    
    return Deterministic(
        troj_res_unif(B=B,
                nu = nu,
                phi_plus = phi_plus,
                phi_minus = phi_minus,
                n_b = n_b
               ),
        name = name,
    )
    
    
