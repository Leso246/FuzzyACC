import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from config import EGO_COLOR, LEADER_COLOR, DATA_COLOR,SECURITY_DISTANCE_ACI, SECURITY_DISTANCE_QUIZ, SIM_CSV_PATH, DATA_CSV_PATH, SIM_LEAD_PLOTS_PATH, SIM_REAL_PLOTS_PATH

# genera i grafici relativi ai dati prodotti dalla simulazione
def generate_sim_plots():

    # Carica i risultati e i dati
    result = pd.read_csv(SIM_CSV_PATH)
    data_df = pd.read_csv(DATA_CSV_PATH)

    data = pd.DataFrame({
        "time": data_df["time"],
        "ego_velocity": data_df["ego_velocity"],
        "ego_acceleration": data_df["acc_acceleration"],
        "actual_ego_acceleration": np.nan,
        "space_gap": data_df["space_gap"],
        "security_distance_quiz": np.nan,
        "security_distance_aci": np.nan
    })


    for i in range(1, len(data_df)):
        time_difference = data_df["time"][i] - data_df["time"][i - 1]
        actual_ego_acceleration = (data_df["ego_velocity"][i] - data_df["ego_velocity"][i - 1]) / time_difference

        data.loc[i, "actual_ego_acceleration"] = actual_ego_acceleration
        data.loc[i, "security_distance_quiz"] = ((data["ego_velocity"][i] * 3.6) / 10) * 3
        data.loc[i, "security_distance_aci"] = pow(((data["ego_velocity"][i] * 3.6) / 10), 2)


    # Grafico ego_velocity simulata VS leader_velocity
    plt.figure(figsize=(16, 8))
    plt.plot(result['time'], result['ego_velocity'], label='Ego Velocity Simulata', color=EGO_COLOR)
    plt.plot(result['time'], result['leader_velocity'], label='Leader Velocity', color=LEADER_COLOR)
    plt.title('Confronto Ego Velocity Simulata e Leader Velocity')
    plt.xlabel('Tempo [s]')
    plt.ylabel('Velocità [m/s]')
    plt.xticks(np.arange(0, 899, step=50))
    plt.legend()
    plt.grid(True)
    plt.savefig(SIM_LEAD_PLOTS_PATH + "/velocity")

    # Grafico ego_acceleration simulata VS leader_acceleration
    plt.figure(figsize=(16, 8))
    plt.plot(result['time'], result['leader_acceleration'], label='Leader Acceleration', color=LEADER_COLOR)
    plt.plot(result['time'], result['ego_acceleration'], label='Ego Acceleration Simulata', color=EGO_COLOR)
    plt.title('Confronto Ego Acceleration Simulata e Leader Acceleration')
    plt.xlabel('Tempo [s]')
    plt.ylabel('Accelerazione [m/s²]')
    plt.xticks(np.arange(0, 899, step=50))
    plt.legend()
    plt.grid(True)
    plt.savefig(SIM_LEAD_PLOTS_PATH + "/acceleration")

    # Grafico space_gap
    plt.figure(figsize=(16, 8))
    plt.plot(result['time'], result['space_gap'], label='Space Gap Simulato', color=EGO_COLOR)
    plt.title('Space Gap simulato nel tempo')
    plt.xlabel('Tempo [s]')
    plt.ylabel('Distanza [m]')
    plt.xticks(np.arange(0, 899, step=50))
    plt.legend()
    plt.grid(True)
    plt.savefig(SIM_LEAD_PLOTS_PATH + "/space_gap")

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
    plt.savefig(SIM_LEAD_PLOTS_PATH + "/space_gap")

    # Grafico space_gap VS security_distance
    plt.figure(figsize=(16, 8))
    plt.plot(result['time'], result['space_gap'], label='Space Gap Simulato', color=EGO_COLOR)
    plt.plot(data['time'], data['security_distance_quiz'], label='Distanza di Sicurezza QuizPatenteApp', color=SECURITY_DISTANCE_QUIZ)
    plt.plot(data['time'], data['security_distance_aci'], label='Distanza di Sicurezza ACI', color=SECURITY_DISTANCE_ACI)
    plt.plot(data['time'], data['space_gap'], label='Spage Gap Reale', color=DATA_COLOR)
    plt.title('Confronto Space Gap Simulato e Reale con Distanze di Sicurezza')
    plt.xlabel('Tempo [s]')
    plt.ylabel('Distanza [m]')
    plt.xticks(np.arange(0, 899, step=50))
    plt.legend()
    plt.grid(True)
    plt.savefig(SIM_LEAD_PLOTS_PATH + "/security_distance")

    # Grafico ego_velocity VS ego_velocity_data
    plt.figure(figsize=(16, 8))
    plt.plot(result['time'], result['ego_velocity'], label='Ego Velocity Simulata', color=EGO_COLOR)
    plt.plot(data['time'], data['ego_velocity'], label='Ego Velocity Reale', color=DATA_COLOR)
    plt.title('Confronto Ego Velocity Simulata e Reale')
    plt.xlabel('Tempo [s]')
    plt.ylabel('Velocità [m/s]')
    plt.xticks(np.arange(0, 899, step=50))
    plt.legend()
    plt.grid(True)
    plt.savefig(SIM_REAL_PLOTS_PATH + "/velocity")

    # Grafico ego_acceleration VS ego_acceleration_impartita
    plt.figure(figsize=(16, 8))
    plt.plot(result['time'], result['ego_acceleration'], label='Ego Acceleration Simulata', color=EGO_COLOR)
    plt.plot(data['time'], data['ego_acceleration'], label='Ego Acceleration Reale Impartita', color=DATA_COLOR)
    plt.title('Confronto Ego Acceleration Simulata e Reale Impartita')
    plt.xlabel('Tempo [s]')
    plt.ylabel('Accelerazione [m/s²]')
    plt.xticks(np.arange(0, 899, step=50))
    plt.legend()
    plt.grid(True)
    plt.savefig(SIM_REAL_PLOTS_PATH + "/acceleration_impartita")

    # Grafico ego_acceleration VS ego_acceleration_data_effettiva
    plt.figure(figsize=(16, 8))
    plt.plot(data['time'], data['actual_ego_acceleration'], label='Ego Acceleration Reale Effettiva', color="#800080")
    plt.plot(result['time'], result['ego_acceleration'], label='Ego Acceleration Simulata', color=EGO_COLOR)
    plt.title('Confronto Ego Acceleration Simulata e Reale Effettiva')
    plt.xlabel('Tempo [s]')
    plt.ylabel('Accelerazione [m/s²]')
    plt.xticks(np.arange(0, 899, step=50))
    plt.legend()
    plt.grid(True)
    plt.savefig(SIM_REAL_PLOTS_PATH + "/acceleration_effettiva")

    # Grafico ego_acceleration_data_impartita VS ego_acceleration_data_effettiva
    plt.figure(figsize=(16, 8))
    plt.plot(data['time'], data['actual_ego_acceleration'], label='Ego Acceleration Reale Effettiva', color="#800080")
    plt.plot(data['time'], data['ego_acceleration'], label='Ego Acceleration Reale Impartita', color=DATA_COLOR)
    plt.title('Confronto Ego Acceleration Reale Simulata ed Effettiva')
    plt.xlabel('Tempo [s]')
    plt.ylabel('Accelerazione [m/s²]')
    plt.xticks(np.arange(0, 899, step=50))
    plt.legend()
    plt.grid(True)
    plt.savefig(SIM_REAL_PLOTS_PATH + "/acceleration_effettiva_impartita")