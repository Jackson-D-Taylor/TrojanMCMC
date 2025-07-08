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

pname = "J0023+0923_synthetic_injected4"
pname_files = pname

print(f"Working on PSR {pname}.")


par = glob.glob(f"./red_noise_and_injected/{pname_files}.par")
tim = glob.glob(f"./red_noise_and_injected/{pname_files}.tim")
psr_real_name = "J0023+0923"


if len(par) != 1 and len(tim) != 1:
    sys.exit("Exiting! More than one par/tim file present for this pulsar!")
psr = Pulsar(par[0], tim[0], timing_package="pint")
model = mb.get_model(par[0])
