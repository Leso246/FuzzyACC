import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import pandas as pd
import matplotlib.pyplot as plt

######################################################
# DEFINISCE L'UNIVERSO

time_headway = ctrl.Antecedent(np.arange(0, 15.1, 0.1), 'time_headway')
relative_velocity = ctrl.Antecedent(np.arange(-20, +20.1, 0.1), 'relative_velocity')
weather_condition = ctrl.Antecedent(np.arange(0, 1.01, 0.01), 'weather_condition')

acceleration = ctrl.Consequent(np.arange(-5, +5.1, 0.1), 'acceleration')

######################################################
# DEFINISCE LE MEMBERSHIP FUNCTIONS

weather_condition['bad'] = fuzz.trapmf(weather_condition.universe, [0.0, 0.0, 0.3, 0.6])
weather_condition['good'] = fuzz.trapmf(weather_condition.universe, [0.4, 0.7, 1.01, 1.01])

time_headway['dangerous'] = fuzz.trapmf(time_headway.universe, [0.0, 0.0, 0.8, 1.2])
time_headway['short'] = fuzz.trimf(time_headway.universe, [1.0, 1.8, 3.0])
time_headway['adequate'] = fuzz.trimf(time_headway.universe, [2.5, 4.0, 5.0])
time_headway['long'] = fuzz.trimf(time_headway.universe, [4.5, 6.0, 7.0])
time_headway['very_long'] = fuzz.trapmf(time_headway.universe, [6.5, 7.0, 15.1, 15.1])

relative_velocity['approaching_fast'] = fuzz.trapmf(relative_velocity.universe, [-20.0, -20.0, -10.0, -5.0])
relative_velocity['approaching'] = fuzz.trimf(relative_velocity.universe, [-7.0, -3.0, -0.5])
relative_velocity['steady'] = fuzz.trimf(relative_velocity.universe, [-1.0, 0.0, 1.0])
relative_velocity['moving_away'] = fuzz.trimf(relative_velocity.universe, [0.5, 3.0, 7.0])
relative_velocity['moving_away_fast'] = fuzz.trapmf(relative_velocity.universe, [5.0, 10.0, 20.1, 20.1])

acceleration['strong_deceleration'] = fuzz.trapmf(acceleration.universe, [-5.0, -5.0, -4.0, -3.0])
acceleration['medium_deceleration'] = fuzz.trimf(acceleration.universe, [-4.0, -3.0, -1.5])
acceleration['light_deceleration'] = fuzz.trimf(acceleration.universe, [-2.0, -1.0, -0.3])
acceleration['zero_acceleration'] = fuzz.trapmf(acceleration.universe, [-0.7, -0.5, 0.5, 0.7])
acceleration['light_acceleration'] = fuzz.trimf(acceleration.universe, [0.3, 1.0, 2.0])
acceleration['medium_acceleration'] = fuzz.trimf(acceleration.universe, [1.5, 3.0, 4.0])
acceleration['strong_acceleration'] = fuzz.trapmf(acceleration.universe, [3.0, 4.0, 5.0, 5.0])

######################################################
# CREA I GRAFICI

# Condizioni Metereologiche
plt.figure(figsize=(10,6))

for label in weather_condition.terms:
    mf = weather_condition[label].mf
    plt.plot(weather_condition.universe, mf, label=label)

plt.title('Membership Functions of Weather Condition')
plt.xlabel('Weather Condition (0=Bad, 1=Good)')
plt.ylabel('Membership Degree')
plt.legend()
plt.grid(True)
plt.savefig("./modello_python/assets/plots/membership_fun/weather_condition")


# Time Headway
plt.figure(figsize=(10,6))

for label in time_headway.terms:
    mf = time_headway[label].mf
    plt.plot(time_headway.universe, mf, label=label)

plt.title('Membership Functions of Time Headway')
plt.xlabel('Time Headway [s]')
plt.ylabel('Membership Degree')
plt.legend()
plt.grid(True)
plt.savefig("./modello_python/assets/plots/membership_fun/time_headway")


# Relative velocity
plt.figure(figsize=(10,6))

for label in relative_velocity.terms:
    mf = relative_velocity[label].mf
    plt.plot(relative_velocity.universe, mf, label=label)

plt.title('Membership Functions of Relative Velocity')
plt.xlabel('Relative Velocity [m/s]')
plt.ylabel('Membership Degree')
plt.legend()
plt.grid(True)
plt.savefig("./modello_python/assets/plots/membership_fun/relative_velocity")

# Acceleration
plt.figure(figsize=(10,6))

for label in acceleration.terms:
    mf = acceleration[label].mf
    plt.plot(acceleration.universe, mf, label=label)

plt.title('Membership Functions of Acceleration')
plt.xlabel('Acceleration [m/s^2]')
plt.ylabel('Membership Degree')
plt.legend()
plt.grid(True)
plt.savefig("./modello_python/assets/plots/membership_fun/acceleration")

######################################################
# CREA LE REGOLE
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

######################################################
# CREA IL SISTEMA DI CONTROLLO

system = ctrl.ControlSystem(rules)
sim = ctrl.ControlSystemSimulation(system)

######################################################
# PASSA GLI INPUT

df = pd.read_csv('modello_python/assets/data/data.csv')

time_column = df['time']
leader_velocity_column = df['leader_velocity']

# Valori inziali
leader_velocity = df['leader_velocity'][0]
ego_velocity = df['ego_velocity'][0]
space_gap = df['space_gap'][0]

ego_acceleration = 0

relative_velocity = leader_velocity - ego_velocity
time_headway = space_gap / ego_velocity

result = pd.DataFrame(
    columns=[
            'time', 
            'ego_velocity', 
            'leader_velocity', 
            'ego_acceleration', 
            'leader_acceleration',
            'space_gap'
            ])

result.loc[0] = [0, ego_velocity, leader_velocity, 0, 0, space_gap]

for index in range(1, len(time_column)):

    time= time_column.iloc[index]

    sim.input['weather_condition'] = 1
    sim.input['relative_velocity'] = relative_velocity
    sim.input['time_headway'] = time_headway

    if abs(relative_velocity) < 1e-3:
        time_headway = 300

    sim.compute()

    # Calcola la differenza di secondi tra uno step e l'altro
    time_difference = time_column[index] - time_column[index - 1]
    
    # Calcola le accelerazioni di entrambe le auto
    ego_acceleration = sim.output['acceleration']

    leader_acceleration = (leader_velocity_column[index] - leader_velocity_column[index - 1]) / time_difference
 
    # Calcola lo spazio in metri percorso da ognuna delle due auto durante uno step di tempo
    ego_travelled_space = ego_velocity * time_difference + 1/2 * ego_acceleration * pow(time_difference, 2)   
    leader_travelled_space =  leader_velocity_column[index - 1] * time_difference + 1/2 *  leader_acceleration * pow(time_difference, 2) 

    # Calcola il nuovo spazio
    space_gap = space_gap + (leader_travelled_space - ego_travelled_space)

    # Calcola la nuova velocità 
    ego_velocity = ego_velocity + ego_acceleration * time_difference
    leader_velocity = leader_velocity_column[index]

    # Calcola la nuova velocità relativa
    relative_velocity = leader_velocity - ego_velocity

    # Calcola il nuovo time headway
    time_headway = space_gap / ego_velocity

    result.loc[index] = [time_column[index], ego_velocity, leader_velocity, ego_acceleration, leader_acceleration, space_gap]

    print(index, ego_acceleration)

result.to_csv("./modello_python/assets/data_sim/sim.csv", index=False)

######################################################