import pandas as pd
import numpy as np
from modello_python.config import SIM_CSV_PATH, DATA_CSV_PATH

# Confronta gli space gap e le distanze di sicurezza

dataset_simulazione_df = pd.read_csv(SIM_CSV_PATH)
dataset_reale_df = pd.read_csv(DATA_CSV_PATH)

data = pd.DataFrame({
    "time": dataset_simulazione_df["time"],
    "ego_velocity_simulata": dataset_simulazione_df["ego_velocity"],
    "ego_velocity_reale":dataset_reale_df["ego_velocity"],
    "space_gap_simulato": dataset_simulazione_df["space_gap"],
    "space_gap_reale": dataset_reale_df["space_gap"],
})

for i in range(1, len(data["time"])):
    time_difference = data["time"][i] - data["time"][i - 1]

    data.loc[i, "security_distance_quiz"] = ((data["ego_velocity_simulata"][i] * 3.6) / 10) * 3
    data.loc[i, "security_distance_aci"] = pow(((data["ego_velocity_simulata"][i] * 3.6) / 10), 2)

diff_simulato_reale = data["space_gap_simulato"] - data["space_gap_reale"]
diff_simulato_reale_mean = np.mean(diff_simulato_reale)
diff_simulato_reale_std = np.std(diff_simulato_reale)

diff_simulato_aci = data["space_gap_simulato"] - data["security_distance_aci"]
diff_simulato_aci_mean = np.mean(diff_simulato_aci)
diff_simulato_aci_std = np.std(diff_simulato_aci)

diff_simulato_quiz = data["space_gap_simulato"] - data["security_distance_quiz"]
diff_simulato_quiz_mean = np.mean(diff_simulato_quiz)
diff_simulato_quiz_std = np.std(diff_simulato_quiz)

print(f"Differenza Simulato vs Reale: media = {diff_simulato_reale_mean:.3f}, std = {diff_simulato_reale_std:.3f}")
print(f"Differenza Simulato vs ACI: media = {diff_simulato_aci_mean:.3f}, std = {diff_simulato_aci_std:.3f}")
print(f"Differenza Simulato vs Quiz: media = {diff_simulato_quiz_mean:.3f}, std = {diff_simulato_quiz_std:.3f}")


