import pandas as pd

df = pd.read_csv("./modello_python/assets/data_sim/sim.csv")

print("Min space gap:", df["space_gap"].min())
print("Max space gap:", df["space_gap"].max())

print("Min relative_velocity:",( df["leader_velocity"] - df["ego_velocity"]).min())
print("Max relative_velocity:", (df["leader_velocity"] - df["ego_velocity"]).max())