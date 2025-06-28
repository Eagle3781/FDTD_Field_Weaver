import os

from sim_modules import *

# CMD Invocation:
"""
cd C:/Users/jonat/OneDrive/01 School/01 UT Dallas/01 Classes/Spring 2025/EERF 6351 Computational Electromagnetics/02 Course Work/FDTD/Python
python FDTD_Field_Weaver.py

"""

def fieldWeaver():
    """
    This function is the main entry point for the FDM simulation.
    It imports the configuration, retrieves parameters, executes the FDM algorithm,
    and graphs the results.
    """
    print("Starting FDM Simulation...")

    config      = configImport()
    environment = getParams(config)
    out         = executeFDM(environment)

    graph(out, environment, config)

if __name__ == "__main__":
    fieldWeaver()
