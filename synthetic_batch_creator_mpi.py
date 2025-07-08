import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("psr")
parser.add_argument("-t", "--temps", default=4, type=int)
parser.add_argument("-niter", "--num_of_iteration", default=int(1e6))

args = parser.parse_args()
psr = args.psr
temps = args.temps
niter = int(float(args.num_of_iteration))

if os.path.exists("/lorule/scratch/jdt00012"):  # for link:
    file_string = (
        "#!/bin/bash\n"
        "\n"
        f"#SBATCH --job-name={psr}\n"
        f"#SBATCH --output={psr}.out\n"
        f"#SBATCH -e {psr}.err\n"
        "#\n"
        f"#SBATCH --ntasks={temps}\n"
        "\n"
        "\n"
        "date\n"
        "module unload python openmpi\n"
        "module load python\n"
        "\n"
        "which python\n"
        "\n"
        f"mpirun -np {temps} python search_troj.py -pname {psr} -mc_min 0.016388 -niter {niter} --synthetic\n"
        "\n"
        "echo all done\n"
        "date"
    )
else:  # for thorny flats:
    file_string = (
        "#!/bin/bash\n"
        "\n"
        f"#SBATCH --job-name={psr}\n"
        f"#SBATCH --output={psr}.out\n"
        f"#SBATCH -e {psr}.err\n"
        "#\n"
        "#SBATCH --partition=comm_small_week\n"
        f"#SBATCH --ntasks={temps}\n"
        "#SBATCH --time=7-00:00:00\n"  # 7 days
        "\n"
        "\n"
        "date\n"
        "echo Running on host: $(hostname)\n"
        "echo Job ID: $SLURM_JOB_ID\n"
        # "module load lang/python/cpython_3.11.3_gcc122\n"
        "module load parallel/openmpi/5.0.2_gcc122\n"
        "module load lang/gcc/12.2.0\n"
        "module load libs/openblas/0.3.26_gcc122\n"
        "source ~/.bashrc\n"
        "micromamba activate trojans\n"
        "\n"
        "\n"
        "which python3\n"
        "\n"
        f"mpirun -np {temps} python3 search_troj.py -pname {psr} -mc_min 0.016388 -niter {niter} --synthetic\n"
        "\n"
        "echo all done\n"
        "date"
    )

with open(f"{psr}.sbatch", "w") as file:
    file.write(file_string)
