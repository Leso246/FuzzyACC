import pandas as pd

df = pd.read_csv("./modello_python/assets/data/data.csv")

print("Initial Ego Velocity: ", df['ego_velocity'][0])
print("Initial Leader Velocity: ", df['leader_velocity'][0])
print("Initial Space Gap: ", df['space_gap'][0])

print("Min leader_velocity:", df["leader_velocity"].min())
print("Max leader_velocity:", df["leader_velocity"].max())