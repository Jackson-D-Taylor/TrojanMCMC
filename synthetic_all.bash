#!/bin/bash

date

for psr in J0023+0923_synthetic_injected4 J0023+0923_synthetic_injected5 J0023+0923_synthetic_injected6 J0023+0923_synthetic_injected7 J0023+0923_synthetic_injected8 J0023+0923_synthetic_no_signal J0023+0923_synthetic_injectedactual

do
    python synthetic_batch_creator.py $psr
    sbatch $psr.sbatch 
done

date