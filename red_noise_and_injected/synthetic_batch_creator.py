import argparse

parser = argparse.ArgumentParser()
parser.add_argument("psr")

args = parser.parse_args()
psr = args.psr

file_string = (
    "#!/bin/bash\n"
    "\n"
    f"#SBATCH --job-name={psr}\n"
    f"#SBATCH --output={psr}.out\n"
    "#\n"
    "#SBATCH --ntasks=1\n"
    "\n"
    "date\n"
    "\n"
    "which python\n"
    "\n"
    f"python search_troj.py -pname {psr} -mc_min 0.016388 --synthetic\n"
    "\n"
    "echo all done\n"
    "date"
)

with open(f"{psr}.sbatch", "w") as file:
    file.write(file_string)
