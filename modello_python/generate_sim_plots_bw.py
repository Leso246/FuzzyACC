import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from config import EGO_COLOR, DATA_COLOR, SIM_CSV_PATH, SIM_BW_CSV_PATH, SIM_EGO_BW_PLOTS_PATH

# Confronto veicolo ego simulato (good weather e bad weather)
dataset_simulazione_df = pd.read_csv(SIM_CSV_PATH)
dataset_simulazione_bw_df = pd.read_csv(SIM_BW_CSV_PATH)

data = pd.DataFrame({
    "time": dataset_simulazione_df["time"],
    "ego_acceleration": dataset_simulazione_df["ego_acceleration"],
    "ego_velocity": dataset_simulazione_df["ego_velocity"],
    "space_gap": dataset_simulazione_df["space_gap"],
    "ego_acceleration_bw":dataset_simulazione_bw_df["ego_acceleration"],
    "ego_velocity_bw": dataset_simulazione_bw_df["ego_velocity"],
    "space_gap_bw": dataset_simulazione_bw_df["space_gap"],
})

# Grafico ego_velocity 
plt.figure(figsize=(16, 8))
plt.plot(data['time'], data['ego_velocity'], label='Ego Velocity (Good Weather)', color=EGO_COLOR)
plt.plot(data['time'], data['ego_velocity_bw'], label='Ego Velocity (Bad Weather)', color=DATA_COLOR)
plt.title('Confronto Ego Velocity Simulata')
plt.xlabel('Tempo [s]')
plt.ylabel('Velocità [m/s]')
plt.xticks(np.arange(0, 899, step=50))
plt.legend()
plt.grid(True)
plt.savefig(SIM_EGO_BW_PLOTS_PATH + "/velocity")

# Grafico Ego Acceleration
plt.figure(figsize=(16, 8))
plt.plot(data['time'], data['ego_acceleration_bw'], label='Ego Acceleration (Bad Weather)', color=DATA_COLOR)
plt.plot(data['time'], data['ego_acceleration'], label='Ego Acceleration (Good Weather)', color=EGO_COLOR)
plt.title('Confronto Ego Acceleration Simulata')
plt.xlabel('Tempo [s]')
plt.ylabel('Accelerazione [m/s²]')
plt.xticks(np.arange(0, 899, step=50))
plt.legend()
plt.grid(True)
plt.savefig(SIM_EGO_BW_PLOTS_PATH + "/acceleration")

# Grafico Space Gap
plt.figure(figsize=(16, 8))
plt.plot(data['time'], data['space_gap'], label='Space Gap (Good Weather)', color=EGO_COLOR)
plt.plot(data['time'], data['space_gap_bw'], label='Space Gap (Bad Weather)', color=DATA_COLOR)
plt.title('Confronto Space Gap Simulato')
plt.xlabel('Tempo [s]')
plt.ylabel('Accelerazione [m/s²]')
plt.xticks(np.arange(0, 899, step=50))
plt.legend()
plt.grid(True)
plt.savefig(SIM_EGO_BW_PLOTS_PATH + "/space_gap")