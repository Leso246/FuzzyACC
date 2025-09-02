# config.py

# Parametro del filtro
ALPHA = 0.1

# Soglia accelerazione
MIN_ACCELERATION = 0.12

# File paths
RULES_CSV_PATH = "./modello_python/rules/rules.csv"
DATA_CSV_PATH = "./modello_python/assets/dataset/dataset_reale.csv"
SIM_CSV_PATH = "./modello_python/assets/dataset_simulation/dataset_simulazione.csv"

MF_PLOTS_PATH = "./modello_python/assets/plots/membership_fun"
SIM_LEAD_PLOTS_PATH = "./modello_python/assets/plots/simulation/leader_comparison"
SIM_REAL_PLOTS_PATH = "./modello_python/assets/plots/simulation/real_data_comparison"

# Colori per i grafici finali
EGO_COLOR = 'blue'
LEADER_COLOR = 'orange'
DATA_COLOR = "#FFD700"
SECURITY_DISTANCE_QUIZ = 'green'
SECURITY_DISTANCE_ACI = '#00CCCC'
