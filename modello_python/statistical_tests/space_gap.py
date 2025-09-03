import pandas as pd
from modello_python.config import SIM_CSV_PATH, DATA_CSV_PATH
from scipy.stats import pearsonr

# Confronta gli space gap

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

