import pandas as pd
from modello_python.config import SIM_CSV_PATH

df = pd.read_csv(SIM_CSV_PATH)

print("Min space gap:", df["space_gap"].min())
print("Max space gap:", df["space_gap"].max())

print("Min relative_velocity:",( df["leader_velocity"] - df["ego_velocity"]).min())
print("Max relative_velocity:", (df["leader_velocity"] - df["ego_velocity"]).max())