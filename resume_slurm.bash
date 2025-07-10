#!/bin/bash

date
module load lang/python/cpython_3.11.3_gcc122

# Default values
t_val="16"
niter_val="5e6"

psr=""
resume_date=""

# Parse args
while [[ $# -gt 0 ]]; do
  case "$1" in
    -t)
      t_val="$2"
      shift 2
      ;;
    -niter)
      niter_val="$2"
      shift 2
      ;;
    -*)
      echo "Unknown option: $1"
      exit 1
      ;;
    *)
      if [ -z "$psr" ]; then
        psr="$1"
      elif [ -z "$resume_date" ]; then
        resume_date="$1"
      else
        echo "Unexpected extra argument: $1"
        exit 1
      fi
      shift
      ;;
  esac
done

# Check required arguments
if [ -z "$psr" ] || [ -z "$resume_date" ]; then
  echo "Usage: $0 <psr> <resume_date> [-t value] [-niter value]"
  exit 1
fi

# Output
echo -e "\nPSR: $psr"
echo -e "Resume date: $resume_date"
echo -e "t value: $t_val"
echo -e "niter value: $niter_val\n"

if [[ "$psr" == *synthetic* ]]; then
  python_script="synthetic_batch_creator_mpi.py $psr -t $t_val -niter $niter_val -rd $resume_date"
else
  python_script="real_batch_creator_mpi.py $psr -t $t_val -niter $niter_val -rd $resume_date"
fi

# Confirm script selection
echo "Selected Python script: $python_script"
read -p "Proceed? [y/n]: " confirm
if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
  echo "Aborted by user."
  exit 1
fi

# Run selected script
echo -e "\n$python_script"
echo -e "$psr.sbatch\n"
python3 "$python_script"
sbatch "$psr.sbatch"

date
