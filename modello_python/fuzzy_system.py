import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import pandas as pd
from config import RULES_CSV_PATH

# Funzione che crea il sistema fuzzy
def create_fuzzy_system():

    ######################################################
    # DEFINISCE L'UNIVERSO

    time_headway = ctrl.Antecedent(np.linspace(0.0, 15.5, num=15000, endpoint=True), 'time_headway')
    relative_velocity = ctrl.Antecedent(np.linspace(-23, +23.0, num=46000, endpoint=True), 'relative_velocity')
    weather_condition = ctrl.Antecedent(np.linspace(0, 1.0, num=1000, endpoint=True), 'weather_condition')

    acceleration = ctrl.Consequent(np.linspace(-3.0, +3.0, num=6000, endpoint=True), 'acceleration')

    ######################################################
    # DEFINISCE LE MEMBERSHIP FUNCTIONS

    weather_condition['bad'] = fuzz.trapmf(weather_condition.universe, [0.0, 0.0, 0.35, 0.65])
    weather_condition['good'] = fuzz.trapmf(weather_condition.universe, [0.35, 0.65, 1.0, 1.0])

    time_headway['dangerous'] = fuzz.trapmf(time_headway.universe, [0.0, 0.0, 0.8, 1.5])
    time_headway['short']    = fuzz.trimf(time_headway.universe, [1.0, 2.0, 3.0])
    time_headway['adequate'] = fuzz.trimf(time_headway.universe, [2.5, 3.75, 5.0])
    time_headway['long']     = fuzz.trimf(time_headway.universe, [4.5, 5.75, 7.0])
    time_headway['very_long'] = fuzz.trapmf(time_headway.universe, [6.5, 7.0, 15.5, 15.5])

    relative_velocity['approaching_fast'] = fuzz.trapmf(relative_velocity.universe, [-23.0, -23.0, -10.0, -5.0])
    relative_velocity['approaching'] = fuzz.trimf(relative_velocity.universe, [-7.0, -3.0, -0.5])
    relative_velocity['steady'] = fuzz.trimf(relative_velocity.universe, [-1.0, 0.0, 1.0])
    relative_velocity['moving_away'] = fuzz.trimf(relative_velocity.universe, [0.5, 3.0, 7.0])
    relative_velocity['moving_away_fast'] = fuzz.trapmf(relative_velocity.universe, [5.0, 10.0, 23.0, 23.0])

    acceleration['strong_deceleration'] = fuzz.trapmf(acceleration.universe, [-3.0, -3.0, -2.5, -2.0])
    acceleration['medium_deceleration'] = fuzz.trimf(acceleration.universe, [-2.5, -1.8, -1.0])
    acceleration['light_deceleration'] = fuzz.trimf(acceleration.universe, [-1.2, -0.7, -0.2])
    acceleration['zero_acceleration'] = fuzz.trapmf(acceleration.universe, [-0.3, -0.1, 0.1, 0.3])
    acceleration['light_acceleration'] = fuzz.trimf(acceleration.universe, [0.2, 0.7, 1.2])
    acceleration['medium_acceleration'] = fuzz.trimf(acceleration.universe, [1.0, 1.8, 2.5])
    acceleration['strong_acceleration'] = fuzz.trapmf(acceleration.universe, [2.0, 2.5, 3.0, 3.0])

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
