# This module handles:
    # Execution of FDM algorithm

import numpy as np

def executeFDM(env):
    """
    ## `executeFDM(env)`

    The `env` parameter should be a dictionary with the following keys:

    ---

    ### 🔌 Field Properties

    - **Conductivity function**  
    → Array defined in space.

    - **Permittivity function** *(electric)*  
    → Array defined in space.

    - **Permeability function** *(magnetic)*  
    → Array defined in space.

    ---

    ### ⚡ Initial Conditions

    - Array defined in space, composed of two sub-arrays:
    - `index 0`: Electric field `E`
    - `index 1`: Magnetic field `H`

    ---

    ### 🧱 Boundary Conditions

    - Same structure as Initial Conditions:
    - `index 0`: Electric field `E`
    - `index 1`: Magnetic field `H`

    ---

    ### 💥 Forcing Functions

    - A **list of arrays**, each array defined in **space and time**
    - Pad with empty lists for consistency
    - This ensures easier access during the FDTD update step

    ---

    ### 📍 Forcing Function Locations

    - Integer array of indices in **space**
    - Example: `[60]` means there is a forcing function at `60 * dx`

    ---

    ### ⏱ Simulation Parameters

    - `time_steps`: *(int)* Total number of time steps
    - `space_steps`: *(int)* Total number of space steps
    - `dx`: *(float)* Spatial resolution
    - `dt`: *(float)* Temporal resolution

    """
    # Extract parameters from the environment dictionary
    sigma       = np.array(env["conductivity"])
    epsilon     = np.array(env["permittivity"])
    mu          = np.array(env["permeability"])
    E0, H0      = env["init_cond"]
    E_bc, H_bc  = env["boundary_cond"]
    sources     = env["forcing_functions"]
    source_locs = env["ff_locations"]
    time_steps  = env["time_steps"]
    space_steps = env["space_steps"]
    dx          = env["dx"]
    dt          = env["dt"]

    # Initialize fields
    E = np.array(E0, dtype=np.float64)
    H = np.array(H0, dtype=np.float64)
    field_history = []

    # Check CFL stability condition
    c   = 1 / np.sqrt(mu * epsilon)
    cfl = np.max(c * dt / dx)
    if cfl > 1.0:
        raise ValueError(f"CFL condition violated: {cfl:.2f} > 1")

    for n in range(time_steps):
        # --- Update H field ---
        for i in range(space_steps - 1):
            H[i] += (dt / (mu[i] * dx)) * (E[i+1] - E[i])

        # --- Update E field ---
        for i in range(1, space_steps - 1):
            E[i] += ((dt / (epsilon[i] * dx)) * (H[i] - H[i-1])) - (dt * sigma[i] / epsilon[i]) * E[i]

        # --- Apply forcing functions ---
        for idx in source_locs:
            if idx < space_steps:
                E[idx] = sources[idx][n]

        # --- Apply boundary conditions ---
        E[0]  = E_bc[0]
        E[-1] = E_bc[1]
        H[0]  = H_bc[0]
        H[-1] = H_bc[1]

        # --- Save field snapshot ---
        field_history.append((E.copy(), H.copy()))

    return field_history

