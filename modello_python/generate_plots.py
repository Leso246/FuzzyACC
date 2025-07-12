import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

EGO_COLOR = 'blue'
LEADER_COLOR = 'orange'
DATA_COLOR = "#E60073"
SECURITY_DISTANCE = 'green'

# Carica i risultati e i dati
result = pd.read_csv("modello_python/assets/data_sim/sim.csv")
data_df = pd.read_csv("modello_python/assets/data/data.csv")

data = pd.DataFrame({
    "time": data_df["time"],
    "ego_velocity": data_df["ego_velocity"],
    "ego_acceleration": np.nan,
    "space_gap": data_df["space_gap"],
    "security_distance": np.nan,
})


for i in range(1, len(data_df)):
    time_difference = data_df["time"][i] - data_df["time"][i - 1]
    ego_acceleration = (data_df["ego_velocity"][i] - data_df["ego_velocity"][i - 1]) / time_difference

    data.loc[i, "ego_acceleration"] = ego_acceleration
    data.loc[i, "security_distance"] = ((data["ego_velocity"][i] * 3.6) / 10) * 3


# Grafico ego_velocity VS leader_velocity
plt.figure(figsize=(16, 8))
plt.plot(result['time'], result['ego_velocity'], label='Ego Velocity', color=EGO_COLOR)
plt.plot(result['time'], result['leader_velocity'], label='Leader Velocity', color=LEADER_COLOR)
plt.title('Confronto Ego Velocity e Leader Velocity')
plt.xlabel('Tempo [s]')
plt.ylabel('Velocità [m/s]')
plt.xticks(np.arange(0, 899, step=50))
plt.legend()
plt.grid(True)
plt.savefig("./modello_python/assets/plots/simulation/leader_comparison/velocity")

# Grafico ego_acceleration VS leader_acceleration
plt.figure(figsize=(16, 8))
plt.plot(result['time'], result['leader_acceleration'], label='Leader Acceleration', color=LEADER_COLOR)
plt.plot(result['time'], result['ego_acceleration'], label='Ego Acceleration', color=EGO_COLOR)
plt.title('Confronto Ego Acceleration e Leader Acceleration')
plt.xlabel('Tempo [s]')
plt.ylabel('Accelerazione [m/s²]')
plt.xticks(np.arange(0, 899, step=50))
plt.legend()
plt.grid(True)
plt.savefig("./modello_python/assets/plots/simulation/leader_comparison/acceleration")

# Grafico space_gap
plt.figure(figsize=(16, 8))
plt.plot(result['time'], result['space_gap'], label='Space Gap Simulato', color=EGO_COLOR)
plt.title('Space Gap simulato nel tempo')
plt.xlabel('Tempo [s]')
plt.ylabel('Distanza [m]')
plt.xticks(np.arange(0, 899, step=50))
plt.legend()
plt.grid(True)
plt.savefig("./modello_python/assets/plots/simulation/leader_comparison/space_gap")

# Grafico ego_velocity VS ego_velocity_data
plt.figure(figsize=(16, 8))
plt.plot(result['time'], result['ego_velocity'], label='Ego Velocity Simulata', color=EGO_COLOR)
plt.plot(data['time'], data['ego_velocity'], label='Ego Velocity Reale', color=DATA_COLOR)
plt.title('Confronto Ego Velocity simulata e reale')
plt.xlabel('Tempo [s]')
plt.ylabel('Velocità [m/s]')
plt.xticks(np.arange(0, 899, step=50))
plt.legend()
plt.grid(True)
plt.savefig("./modello_python/assets/plots/simulation/real_data_comparison/velocity")

# Grafico ego_acceleration VS ego_acceleration_data
plt.figure(figsize=(16, 8))
plt.plot(data['time'], data['ego_acceleration'], label='Ego Acceleration Reale', color=DATA_COLOR)
plt.plot(result['time'], result['ego_acceleration'], label='Ego Acceleration Simulata', color=EGO_COLOR)
plt.title('Confronto Ego Acceleration simulata e reale')
plt.xlabel('Tempo [s]')
plt.ylabel('Accelerazione [m/s²]')
plt.xticks(np.arange(0, 899, step=50))
plt.legend()
plt.grid(True)
plt.savefig("./modello_python/assets/plots/simulation/real_data_comparison/acceleration")

# Grafico space_gap VS space_gap_data
plt.figure(figsize=(16, 8))
plt.plot(result['time'], result['space_gap'], label='Space Gap Simulato', color=EGO_COLOR)
plt.plot(data['time'], data['space_gap'], label='Spage Gap Reale', color=DATA_COLOR)
plt.title('Confronto Space Gap simulato e reale')
plt.xlabel('Tempo [s]')
plt.ylabel('Distanza [m]')
plt.xticks(np.arange(0, 899, step=50))
plt.legend()
plt.grid(True)
plt.savefig("./modello_python/assets/plots/simulation/real_data_comparison/space_gap")

# Grafico space_gap VS security_distance
plt.figure(figsize=(16, 8))
plt.plot(result['time'], result['space_gap'], label='Space Gap Simulato', color=EGO_COLOR)
plt.plot(data['time'], data['security_distance'], label='Distanza di Sicurezza', color=SECURITY_DISTANCE)
plt.title('Confronto Space Gap simulato e Distanza di Sicurezza')
plt.xlabel('Tempo [s]')
plt.ylabel('Distanza [m]')
plt.xticks(np.arange(0, 899, step=50))
plt.legend()
plt.grid(True)
plt.savefig("./modello_python/assets/plots/simulation/real_data_comparison/security_distance")