#!/bin/bash

date

module load lang/python/cpython_3.11.3_gcc122

for psr in J0023+0923 J0610-2100 J0636+5128 J1719-1438 J1745+1017 J2214+3000 J2234+0944

do
    python3 real_batch_creator_mpi.py $psr -t $1 -niter $2 # -t is number of temperatures and -niter is number of MCMC steps (like 1e6; and yes, 1e6 notation is accepted here)
    sbatch $psr.sbatch 
done

date