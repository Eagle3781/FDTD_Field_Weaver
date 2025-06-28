import numpy as np

from sim_modules import *

# CMD Invocation:
"""
cd C:/Users/jonat/OneDrive/01 School/01 UT Dallas/01 Classes/Spring 2025/EERF 6351 Computational Electromagnetics/02 Course Work/FDTD/Python
python main.py

"""

config      = configImport()
environment = getParams(config)
out         = executeFDM(environment)

graph(out, environment, config)
