from mpi4py import MPI
import argparse
print("in python script | argparse imported")

comm = MPI.COMM_WORLD

MPIrank = comm.Get_rank()
nchain = comm.Get_size()

print(f"{MPIrank=}")
print(f"{nchain=}")

parser = argparse.ArgumentParser()
parser.add_argument("-pname", "--pulsar_name", type=str)
args = parser.parse_args()
pname = args.pulsar_name
print(f"pname = {pname}")