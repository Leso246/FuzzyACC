import pandas as pd
from modello_python.config import SIM_CSV_PATH, DATA_CSV_PATH
from scipy.stats import pearsonr

# Confronta la ego acceleration simulata con la la ego acceleration impartita

dataset_simulazione_df = pd.read_csv(SIM_CSV_PATH)
dataset_reale_df = pd.read_csv(DATA_CSV_PATH)

data = pd.DataFrame({
    "ego_acceleration_sim": dataset_simulazione_df["ego_acceleration"],
    "ego_acceleration_impartita": dataset_reale_df["acc_acceleration"]
})

# Calcola la correlazione di Pearson per le accelerazioni
corr, _ = pearsonr(data["ego_acceleration_sim"], data["ego_acceleration_impartita"])
print('Correlazione di Pearson per le accelerazioni: %.3f' % corr)