import numpy as np

# This module handles:
    # the material properties
    # Stability requirements
    # Differential calculations

def getParams(config):

    environment = {}

    c                 = config["constants"]["c"]
    epsilon_0         = config["constants"]["epsilon_0"]
    mu_0              = config["constants"]["mu_0"]
    length            = config["general"]["length"]
    sim_time_steps    = config["general"]["sim_time_steps"]
    sim_space_steps   = config["general"]["sim_space_steps"]
    forcing_functions = config["forcing_functions"]

    # List used to create the initial conditions array
    # The indices of each entry correspond to the indices of 
    # the functions given in config["forcing_functions"]
    init_cond_values = []

    def differentials():
        # For this run, dx = wavelength/20
        # wavelength = c/f
        dx = 0.0075
        dt = dx/(2*c)
        environment["dx"] = dx
        environment["dt"] = dt
    
    def forcingFunctions():
        # Note: This will only specify electric field forcing functions

        ff_locations     = []

        # Initialize a 2D array of zeros
        FF = []
        # use empty lists to save space
        # x  = np.zeros(sim_space_steps)
        x  = []
        for n in range(sim_time_steps):
            FF.append(x)

        # Generate function data for each function listed in config.json
        for i in forcing_functions:
            # unpack dictionary
            f_x           = i["location"]
            function_type = i["function_type"]
            
            ff_locations.append(f_x)

            # Determine the type of forcing function
            if   function_type == "cos":
                f  = i["frequency"]
                w  = 2*np.pi*f
                t  = np.linspace(0, length, sim_time_steps)
                ff = list(np.cos(w*t))

            elif function_type == "sin":
                f  = i["frequency"]
                w  = 2*np.pi*f
                t  = np.linspace(0, length, sim_time_steps)
                ff = list(np.sin(w*t))

            # delta function
            else:
                ff    = list(np.zeros(sim_time_steps))
                ff[0] = 1

            init_cond_values.append(ff[0])
            FF[f_x] = ff

        # Package the environment dictionary
        environment["forcing_functions"] = FF
        environment["ff_locations"]      = ff_locations
        environment["time_steps"]        = sim_time_steps
        environment["space_steps"]       = sim_space_steps

    def permeability():
        perm = []
        for i in range(sim_space_steps):
            perm.append(mu_0)
        environment["permeability"] = perm

    def permittivity():
        perm = []
        for i in range(sim_space_steps):
            perm.append(epsilon_0)
        environment["permittivity"] = perm

    def conductance():
        cond = []
        for i in range(sim_space_steps):
            # cond.append(1)
            cond.append(0)
        environment["conductivity"] = cond

    def boundary_cond():
        environment["boundary_cond"] = config["boundary_conditions"]

    def initConditions():
        # Composed of two arrays. index zero is the E field, index 1 is the H field
        init_cond = [
            # E Field
            [],
            # H Field:
            []
        ]

        # initialize each list (makes the indices writable):
        x = np.zeros(sim_space_steps)
        init_cond[0] = list(x)
        init_cond[1] = list(x)

        j = 0
        for i in environment["ff_locations"]:
            init_cond[0][i] = init_cond_values[j]
            j += 1
        
        environment["init_cond"] = init_cond

    differentials()
    forcingFunctions()
    permeability()
    permittivity()
    conductance()
    boundary_cond()
    initConditions()

    return environment

