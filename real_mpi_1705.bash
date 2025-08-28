#!/bin/bash

date

module load lang/python/cpython_3.11.3_gcc122

for psr in J1705-1903

do
    python3 real_batch_creator_mpi.py $psr -t $1 -niter $2 # -t is number of temperatures and -niter is number of MCMC steps (like 1e6; and yes, 1e6 notation is accepted here)
    sbatch $psr.sbatch 
done

date