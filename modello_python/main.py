import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import pandas as pd
import matplotlib.pyplot as plt

# distance_m = ...      # es. 60
# ego_speed_m_s = ...   # es. 30 (108 km/h)
# lead_speed_m_s = ...  # es. 25 (90 km/h)

# # Calcola time headway
# time_headway_value = distance_m / ego_speed_m_s

# # Calcola relative velocity
# relative_velocity_value = ego_speed_m_s - lead_speed_m_s

######################################################
# DEFINISCO L'UNIVERSO

time_headway = ctrl.Antecedent(np.arange(0, 15, 0.1), 'time_headway')
relative_velocity = ctrl.Antecedent(np.arange(-20, +20, 0.1), 'relative_velocity')
weather_condition = ctrl.Antecedent(np.arange(0, 1.01, 0.01), 'weather_condition')

acceleration = ctrl.Consequent(np.arange(-5, 5, 0.1), 'acceleration')

######################################################
# DEFINISCO LE MEMBERSHIP FUNCTIONS

weather_condition['bad'] = fuzz.trimf(weather_condition.universe, [0, 0.33, 0.66])
weather_condition['good'] = fuzz.trimf(weather_condition.universe, [0.33, 0.66, 1])

time_headway['dangerous'] = fuzz.trapmf(time_headway.universe, [0, 0, 0.8, 1.5])
time_headway['short'] = fuzz.trimf(time_headway.universe, [1, 2, 3])
time_headway['adequate'] = fuzz.trimf(time_headway.universe, [2.5, 4, 6])
time_headway['long'] = fuzz.trimf(time_headway.universe, [5, 7, 10])
time_headway['very_long'] = fuzz.trapmf(time_headway.universe, [9, 12, 15, 15])

relative_velocity['approaching_fast'] = fuzz.trapmf(relative_velocity.universe, [-20, -20, -10, -5])
relative_velocity['approaching'] = fuzz.trimf(relative_velocity.universe, [-7, -3, 0])
relative_velocity['steady'] = fuzz.trimf(relative_velocity.universe, [-1, 0, 1])
relative_velocity['moving_away'] = fuzz.trimf(relative_velocity.universe, [0, 3, 7])
relative_velocity['moving_away_fast'] = fuzz.trapmf(relative_velocity.universe, [5, 10, 20, 20])

acceleration['strong_deceleration'] = fuzz.trapmf(acceleration.universe, [-5, -5, -4, -3])
acceleration['medium_deceleration'] = fuzz.trimf(acceleration.universe, [-4, -3, -1.5])
acceleration['light_deceleration'] = fuzz.trimf(acceleration.universe, [-2, -1, -0.3])
acceleration['zero_acceleration'] = fuzz.trapmf(acceleration.universe, [-0.5, -0.3, 0.3, 0.5])
acceleration['light_acceleration'] = fuzz.trimf(acceleration.universe, [0.3, 1, 2])
acceleration['medium_acceleration'] = fuzz.trimf(acceleration.universe, [1.5, 3, 4])
acceleration['strong_acceleration'] = fuzz.trapmf(acceleration.universe, [3, 4, 5, 5])

######################################################
# CREA I GRAFICI

# Condizioni Metereologiche
# plt.figure(figsize=(10,6))

# for label in weather_condition.terms:
#     mf = weather_condition[label].mf
#     plt.plot(weather_condition.universe, mf, label=label)

# plt.title('Membership Functions of Weather Condition')
# plt.xlabel('Weather Condition (0=Bad, 1=Good)')
# plt.ylabel('Membership Degree')
# plt.legend()
# plt.grid(True)
# plt.show()


# Time Headway
# plt.figure(figsize=(10,6))

# for label in time_headway.terms:
#     mf = time_headway[label].mf
#     plt.plot(time_headway.universe, mf, label=label)

# plt.title('Membership Functions of Time Headway')
# plt.xlabel('Time Headway [s]')
# plt.ylabel('Membership Degree')
# plt.legend()
# plt.grid(True)
# plt.show()


# Relative velocity
# plt.figure(figsize=(10,6))

# for label in relative_velocity.terms:
#     mf = relative_velocity[label].mf
#     plt.plot(relative_velocity.universe, mf, label=label)

# plt.title('Membership Functions of Relative Velocity')
# plt.xlabel('Relative Velocity [m/s]')
# plt.ylabel('Membership Degree')
# plt.legend()
# plt.grid(True)
# plt.show()

# Acceleration
# plt.figure(figsize=(10,6))

# for label in acceleration.terms:
#     mf = acceleration[label].mf
#     plt.plot(acceleration.universe, mf, label=label)

# plt.title('Membership Functions of Acceleration')
# plt.xlabel('Acceleration [m/s^2]')
# plt.ylabel('Membership Degree')
# plt.legend()
# plt.grid(True)
# plt.show()

######################################################
# CREO LE REGOLE
df = pd.read_csv('./modello_python/rules.csv')

rules = []
for _, row in df.iterrows():
    # Controlli di validazione
    assert row['weather_condition'] in weather_condition.terms, f"Errore: '{row['weather_condition']}' non è una weather_condition valida."
    assert row['time_headway'] in time_headway.terms, f"Errore: '{row['time_headway']}' non è un time_headway valido."
    assert row['relative_velocity'] in relative_velocity.terms, f"Errore: '{row['relative_velocity']}' non è una relative_velocity valida."
    assert row['acceleration'] in acceleration.terms, f"Errore: '{row['acceleration']}' non è un acceleration valido."


    rule = ctrl.Rule(
        antecedent=(
            (weather_condition[row['weather_condition']] &
             time_headway[row['time_headway']] &
             relative_velocity[row['relative_velocity']])
        ),
        consequent=acceleration[row['acceleration']],
        label=f"{row['weather_condition']}_{row['time_headway']}_{row['relative_velocity']}"
    )
    rules.append(rule)