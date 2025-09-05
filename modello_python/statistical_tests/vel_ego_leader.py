import pandas as pd
from modello_python.config import SIM_CSV_PATH
from scipy.stats import pearsonr

# Confronta la ego velocity simulata con la leader velocity

dataset_df = pd.read_csv(SIM_CSV_PATH)

data = pd.DataFrame({
    "ego_velocity": dataset_df["ego_velocity"],
    "leader_velocity": dataset_df["leader_velocity"],
})

# Calcola la correlazione di Pearson per le velocità
corr, _ = pearsonr(data["ego_velocity"], data["leader_velocity"])
print('Pearsons correlation per le velocità: %.3f' % corr)