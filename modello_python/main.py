# main.py

from fuzzy_system import create_fuzzy_system
from generate_mf_plots import  generate_mf_plots
from simulation import run_simulation
from generate_sim_plots import generate_sim_plots

if __name__ == "__main__":
    system, weather_condition, time_headway, relative_velocity, acceleration = create_fuzzy_system()

    # Plotta le Membership Functrions
    generate_mf_plots(
        weather_condition, 
        "Weather Condition", 
        "Weather Condition (0=Bad, 1=Good)", 
        "/weather_condition", 
        tight_legend=False
    )
    
    generate_mf_plots(
        time_headway, 
        "Time Headway", 
        "Time Headway [s]", 
         "/time_headway", 
        tight_legend=False
    )

    generate_mf_plots(
        relative_velocity, 
        "Relative Velocity", 
        "Relative Velocity [m/s]", 
        "/relative_velocity", 
        tight_legend=False
    )

    generate_mf_plots(
        acceleration, 
        "Acceleration", 
        "Accelerazione [m/s²]", 
        "/acceleration", 
        tight_legend=True
    )


    # Avvia la simulazione
    run_simulation(system)

    # Genera i plots relativi ai dati prodotti dalla simulazione
    generate_sim_plots()