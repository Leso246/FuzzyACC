# generate_mf_plots.py

import matplotlib.pyplot as plt
from config import MF_PLOTS_PATH

# Genera i grafici delle membership functions
def generate_mf_plots(var, title, xlabel, output_path, tight_legend):
    plt.figure(figsize=(10, 6))

    for label in var.terms:
        mf = var[label].mf
        plt.plot(var.universe, mf, label=label)

    plt.title('Membership Functions di ' + title)
    plt.xlabel(xlabel)
    plt.ylabel('Grado di Appartenenza')

    if tight_legend: 
        plt.legend(loc="upper left", bbox_to_anchor=(1, 1))
        plt.tight_layout()
    else:
        plt.legend()

    plt.grid(True)
    plt.savefig(MF_PLOTS_PATH + output_path)
    plt.close()
