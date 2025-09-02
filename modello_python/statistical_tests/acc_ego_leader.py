import pandas as pd
from modello_python.config import SIM_CSV_PATH, ALPHA
from scipy.stats import pearsonr

dataset_df = pd.read_csv(SIM_CSV_PATH)

data = pd.DataFrame({
    "ego_acceleration": dataset_df["ego_acceleration"],
    "leader_acceleration": dataset_df["leader_acceleration"],
})

filtered = [data["leader_acceleration"].iloc[0]]

for i in range(1, len(data)):
    new_val = ALPHA * data["leader_acceleration"].iloc[i] + (1 - ALPHA) * filtered[-1]
    filtered.append(new_val)

data["leader_acceleration_filtered"] = filtered

# Calcola la correlazione di Pearson per le accelerazioni
corr, _ = pearsonr(data["ego_acceleration"], data["leader_acceleration_filtered"])
print('Correlazione di Pearson per le accelerazioni: %.3f' % corr)