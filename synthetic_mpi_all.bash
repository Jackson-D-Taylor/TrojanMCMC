#!/bin/bash

date

for psr in J0023+0923_synthetic_injected4 J0023+0923_synthetic_injected5 J0023+0923_synthetic_injected6 J0023+0923_synthetic_injected7 J0023+0923_synthetic_injected8 J0023+0923_synthetic_no_signal J0023+0923_synthetic_injectedactual

do
    python synthetic_batch_creator_mpi.py $psr -t $1 -niter $2 # -t is number of temperatures and -niter is number of MCMC steps (like 1e6)
    sbatch $psr.sbatch
done

date