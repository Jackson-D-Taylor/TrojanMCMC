import argparse

parser = argparse.ArgumentParser()
parser.add_argument("psr")

args = parser.parse_args()
psr = args.psr

B_lim_str = ""
if "unifB" in psr:
    B_lim_small = int(psr[-7])
    B_lim_str = f" --B_lim {B_lim_small+0.5},{B_lim_small-0.5}"

print(f"In batchcretor: {B_lim_str=}")

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
    f"python search_troj.py -pname {psr} -mc_min 0.016388 --synthetic{B_lim_str}\n"
    "\n"
    "echo all done\n"
    "date"
)

with open(f"{psr}.sbatch", "w") as file:
    file.write(file_string)
