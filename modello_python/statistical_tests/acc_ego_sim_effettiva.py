import pandas as pd
from modello_python.config import SIM_CSV_PATH, DATA_CSV_PATH
from scipy.stats import pearsonr

# Confronta la ego acceleration simulata con la la ego acceleration effettiva

dataset_simulazione_df = pd.read_csv(SIM_CSV_PATH)
dataset_reale_df = pd.read_csv(DATA_CSV_PATH)

data = pd.DataFrame({
    "ego_acceleration_sim": dataset_simulazione_df["ego_acceleration"],
    "ego_velocity_reale": dataset_reale_df["ego_velocity"]
})

ego_acceleration_effettiva = [0]

for i in range (1, len(data["ego_velocity_reale"])):
    new_val = (data["ego_velocity_reale"][i] - data["ego_velocity_reale"][i-1])/(0.1)
    ego_acceleration_effettiva.append(new_val)

data["ego_acceleration_effettiva"] = ego_acceleration_effettiva

# Calcola la correlazione di Pearson per le accelerazioni
corr, _ = pearsonr(data["ego_acceleration_sim"], data["ego_acceleration_effettiva"])
print('Correlazione di Pearson per le accelerazioni: %.3f' % corr)