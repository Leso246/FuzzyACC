import pandas as pd
from modello_python.config import SIM_CSV_PATH, DATA_CSV_PATH
from scipy.stats import pearsonr

# Confronta la ego velocity simulata con la leader velocity

dataset_simulazione_df = pd.read_csv(SIM_CSV_PATH)
dataset_reale_df = pd.read_csv(DATA_CSV_PATH)

data = pd.DataFrame({
    "ego_velocity_simulata": dataset_simulazione_df["ego_velocity"],
    "ego_velocity_reale": dataset_reale_df["ego_velocity"],
})

# Calcola la correlazione di Pearson per le velocità
corr, _ = pearsonr(data["ego_velocity_simulata"], data["ego_velocity_reale"])
print('Pearsons correlation per le velocità: %.3f' % corr)