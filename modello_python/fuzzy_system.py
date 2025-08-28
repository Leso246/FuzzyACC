import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import pandas as pd
from config import RULES_CSV_PATH

# Funzione che crea il sistema fuzzy
def create_fuzzy_system():

    ######################################################
    # DEFINISCE L'UNIVERSO

    time_headway = ctrl.Antecedent(np.arange(0, 15.6, 0.1), 'time_headway')
    relative_velocity = ctrl.Antecedent(np.arange(-20, +20.1, 0.1), 'relative_velocity')
    weather_condition = ctrl.Antecedent(np.arange(0, 1.01, 0.01), 'weather_condition')

    acceleration = ctrl.Consequent(np.arange(-3.0, +3.1, 0.1), 'acceleration')

    ######################################################
    # DEFINISCE LE MEMBERSHIP FUNCTIONS

    weather_condition['bad'] = fuzz.trapmf(weather_condition.universe, [0.0, 0.0, 0.3, 0.6])
    weather_condition['good'] = fuzz.trapmf(weather_condition.universe, [0.4, 0.7, 1.01, 1.01])

    time_headway['dangerous'] = fuzz.trapmf(time_headway.universe, [0.0, 0.0, 0.8, 1.2])
    time_headway['short'] = fuzz.trimf(time_headway.universe, [1.0, 1.8, 3.0])
    time_headway['adequate'] = fuzz.trimf(time_headway.universe, [2.5, 4.0, 5.0])
    time_headway['long'] = fuzz.trimf(time_headway.universe, [4.5, 6.0, 7.0])
    time_headway['very_long'] = fuzz.trapmf(time_headway.universe, [6.5, 7.0, 15.6, 15.6])

    relative_velocity['approaching_fast'] = fuzz.trapmf(relative_velocity.universe, [-20.0, -20.0, -10.0, -5.0])
    relative_velocity['approaching'] = fuzz.trimf(relative_velocity.universe, [-7.0, -3.0, -0.5])
    relative_velocity['steady'] = fuzz.trimf(relative_velocity.universe, [-1.0, 0.0, 1.0])
    relative_velocity['moving_away'] = fuzz.trimf(relative_velocity.universe, [0.5, 3.0, 7.0])
    relative_velocity['moving_away_fast'] = fuzz.trapmf(relative_velocity.universe, [5.0, 10.0, 20.1, 20.1])

    acceleration['strong_deceleration'] = fuzz.trapmf(acceleration.universe, [-3.0, -3.0, -2.5, -2.0])
    acceleration['medium_deceleration'] = fuzz.trimf(acceleration.universe, [-2.5, -1.8, -1.0])
    acceleration['light_deceleration'] = fuzz.trimf(acceleration.universe, [-1.2, -0.7, -0.2])
    acceleration['zero_acceleration'] = fuzz.trapmf(acceleration.universe, [-0.3, -0.1, 0.1, 0.3])
    acceleration['light_acceleration'] = fuzz.trimf(acceleration.universe, [0.2, 0.7, 1.2])
    acceleration['medium_acceleration'] = fuzz.trimf(acceleration.universe, [1.0, 1.8, 2.5])
    acceleration['strong_acceleration'] = fuzz.trapmf(acceleration.universe, [2.0, 2.5, 3.1, 3.1])

    ######################################################
    # CREA LE REGOLE

    df = pd.read_csv(RULES_CSV_PATH)

    rules = []
    for _, row in df.iterrows():

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

    ######################################################

    return system, weather_condition, time_headway, relative_velocity, acceleration
