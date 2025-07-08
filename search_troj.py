import numpy as np
import json
import argparse
import glob
import sys
import shutil
import os
from datetime import datetime

from enterprise.pulsar import Pulsar
import enterprise.signals.parameter as parameter
from enterprise.signals.parameter import Uniform
from enterprise.signals import selections
from enterprise.signals import white_signals
from enterprise.signals.gp_signals import MarginalizingTimingModel
from enterprise_extensions import blocks

from troj_signal_a_term import troj_res_block
from custom_priors import AuxiliaryCircularJump
from enterprise.signals import signal_base

from PTMCMCSampler.PTMCMCSampler import PTSampler as ptmcmc
import pint.models.model_builder as mb

parser = argparse.ArgumentParser()
parser.add_argument("-pname", "--pulsar_name", type=str)
parser.add_argument(
    "-mc_min",
    "--m_c_min_mass",
    type=float,
)
parser.add_argument("-niter", "--num_of_iteration", default=int(1e6), type=int)
parser.add_argument(
    "--synthetic",
    help="Whether NG 15yr or injected (synthetic) toas",
    action=argparse.BooleanOptionalAction,
    type=bool,
    default=False,
)

args = parser.parse_args()
pname = args.pulsar_name
pname_files = pname
niter = args.num_of_iteration
mc_min = args.m_c_min_mass

print(f"Working on PSR {pname}.")

if args.synthetic:
    par = glob.glob(f"./red_noise_and_injected/{pname_files}.par")
    tim = glob.glob(f"./red_noise_and_injected/{pname_files}.tim")
    psr_real_name = "J0023+0923"
else:
    par = glob.glob(f"./data/par/{pname}_PINT_*.nb.par")
    tim = glob.glob(f"./data/tim/{pname}_PINT_*.nb.tim")
    psr_real_name = pname


if len(par) != 1 and len(tim) != 1:
    sys.exit("Exiting! More than one par/tim file present for this pulsar!")
psr = Pulsar(par[0], tim[0], timing_package="pint")
model = mb.get_model(par[0])
f_b = (
    model.FB0.value
)  # no factor of 86400 because ENTERPRISE uses units of seconds for TOAs
if f_b is None:
    P_b_days = model.PB.value
    P_b_seconds = P_b_days * 86400
    f_b = 1 / P_b_seconds

n_b_Const = parameter.Constant(f_b * np.pi * 2)("n_b")
n_b = f_b * np.pi * 2
# n_b = f_b * np.pi*2

m_p = 1.35
mu_max = 1 / 27 * 1.1
mu_min = mc_min / (mc_min + m_p) * 0.8
nu_min = n_b * np.sqrt(27 / 4 * mu_min)
# nu_max = n_b * np.sqrt(27/4 * mu_max)

# kappa = (1.4 - mc_min) / (1.4 + mc_min)
# nu_min = 1/10 * n_b/2 * np.sqrt(2 - np.sqrt(27*kappa**2 - 23))
nu_max = n_b * np.sqrt(2) / 2 * 1.2  # this is larger than the other nu_max

tmin = psr.toas.min()
tmax = psr.toas.max()
T_asc = model.TASC.value * 86400  # convert from days to seconds
T_asc_Const = parameter.Constant(T_asc)("T_asc")
Tspan = tmax - tmin
print(f"Tspan for {pname} =  {Tspan/(365.25*86400)} years.")

# define selection by observing backend
selection = selections.Selection(selections.by_backend)

# white noise parameters
efac = parameter.Constant()
equad = parameter.Constant()
ecorr = parameter.Constant()


efeq = white_signals.MeasurementNoise(
    efac=efac, log10_t2equad=equad, selection=selection
)
ec = white_signals.EcorrKernelNoise(log10_ecorr=ecorr, selection=selection)

tm = MarginalizingTimingModel(use_svd=True)
rn = blocks.red_noise_block(psd="powerlaw", components=30)

if args.synthetic and pname[-1] in "45":
    troj = troj_res_block(
        nu=Uniform(nu_min, nu_max),
        n_b=n_b_Const,
        log_B=Uniform(-12, -3.5),
        T_asc=T_asc_Const,
    )
else:
    troj = troj_res_block(nu=Uniform(nu_min, nu_max), n_b=n_b_Const, T_asc=T_asc_Const)

signal_model = tm + efeq + ec + rn + troj
pta = signal_base.PTA(signal_model(psr))

noisedict = json.load(open("./data/15year_noise_dict.json", "r"))

# set white noise parameters with dictionary
pta.set_default_params(noisedict)
print(pta.summary())
print(f"param names = {pta.param_names}")
print(f"nu_min = {nu_min}, nu_max = {nu_max}")

x0 = np.hstack([p.sample() for p in pta.params])
print(f"x0 = {x0}")
print(f"lnprior at x0 = {pta.get_lnprior(x0)}")
print(f"lnlikelihood at x0 = {pta.get_lnlikelihood(x0)}")

ndim = len(x0)

# set up the sampler:
# initial jump covariance matrix
cov = np.diag(np.ones(ndim) * 0.001**2)

# B_lim_name = "unifB_" if B_lim else ""
# Get today's date and format it as "25Feb_2025"
formatted_date = datetime.today().strftime("%d%b_%Y")
#

top_chaindir = "/lorule/scratch/jdt00012"  # lorule scratch directory
if not os.path.exists(top_chaindir):
    top_chaindir = "/scratch/jdt00012"  # switch to the Thorny Flats scratch directory
if not os.path.exists(top_chaindir):
    sys.exit("Error: scratch directory does not exist")
chaindir = f"{top_chaindir}/chains_{formatted_date}/{pname}/"


sampler = ptmcmc(
    ndim, pta.get_lnlikelihood, pta.get_lnprior, cov, outDir=chaindir, resume=False
)

# this enforces theta, phi within [0, 2pi] by sending theta to theta % (2pi) and phi to phi % (2pi),
# rather than rejecting proposals that would take theta or phi outside of [0, 2pi]
circ_aux_jump = AuxiliaryCircularJump(pta)
sampler.addAuxilaryJump(circ_aux_jump)

sampler.sample(
    x0,
    niter,
    maxIter=int(4 * niter),
    writeHotChains=True,
    hotChain=True,
    SCAMweight=4,
    AMweight=2,
    DEweight=15,
)
shutil.move(f"{pname}.out", f"{chaindir}/{pname}.out")
