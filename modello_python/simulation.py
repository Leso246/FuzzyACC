import pandas as pd
from skfuzzy import control as ctrl
from config import DATA_CSV_PATH, SIM_CSV_PATH, ALPHA, MIN_ACCELERATION

# Esegue la simulazione
def run_simulation(system):

    sim = ctrl.ControlSystemSimulation(system)

    ######################################################
    # PASSA GLI INPUT

    df = pd.read_csv(DATA_CSV_PATH)

    time_column = df['time']
    leader_velocity_column = df['leader_velocity']

    # Valori inziali
    leader_velocity =  leader_velocity_column[0]
    ego_velocity = df['ego_velocity'][0]
    space_gap = df['space_gap'][0]

    ego_acceleration = 0
    filtered_acceleration = 0

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

        time = time_column.iloc[index]

        sim.input['weather_condition'] = 1
        sim.input['relative_velocity'] = relative_velocity
        sim.input['time_headway'] = time_headway

        sim.compute()

        # Calcola la differenza di secondi tra uno step e l'altro
        time_difference = time_column[index] - time_column[index - 1]

        # Calcola l'accelerazione del modello fuzzy
        ego_acceleration_fuzzy = sim.output['acceleration']
    
        # Exponentially-Weighted Moving Average (https://www.geogebra.org/m/tb88mqrm)
        filtered_acceleration = ALPHA * ego_acceleration_fuzzy + (1 - ALPHA) * filtered_acceleration

        ego_acceleration = filtered_acceleration

        # Se il modulo dell'accelerazione è troppo basso, riporto a zero
        if(abs(ego_acceleration)) < MIN_ACCELERATION:
            ego_acceleration = 0
        else:
            ego_acceleration

        # Calcola la leader acceleration
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

        result.loc[index] = [
            time, 
            ego_velocity, 
            leader_velocity, 
            ego_acceleration, 
            leader_acceleration, 
            space_gap
        ]

        print("index: ", index, " acceleration: ", ego_acceleration)
    
    result.to_csv(SIM_CSV_PATH, index=False)

