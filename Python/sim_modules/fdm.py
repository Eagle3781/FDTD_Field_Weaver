import numpy as np

# This module handles:
    # Execution of FDM algorithm


def executeFDM(environment):
    # Environment should be a dict containing:
        # Conductivity function      (array in space)
        # Permittivity function      (array in space) (electric)
        # Permeability function      (array in space) (magnetic)
        # Initial Conditions         (array in space)
            # Composed of two arrays. index zero is the E field, index 1 is the H field

        # Boundary Conditions        (array in space)
            # Format the same as the initial conditions
            # index zero is the E field
            # index 1 is the H field

        # Forcing functions          (list of arrays in space and time)
            # pad with empty lists
            # This is to ensure easier access in the FDTD algorithm

        # Forcing Function Locations
            # Integer array that contains the indices of the forcing functions
            # if the array contains a 60 at index zero, that means that there is a forcing function in space at 60dx
            # Simply append the list with the location of forcing functions in space
           

        # Time steps                 (Integer) Total number of steps in time
        # Space steps                (Integer) Total number of steps in space
        # dx                         (float)   spatial differential
        # dt                         (float)   temporal differential

    # Unpack the dictionary:
    s                 = environment["conductivity"]
    e                 = environment["permittivity"]
    u                 = environment["permeability"]
    boundary_cond     = environment["boundary_cond"]
    init_cond         = environment["init_cond"]
    forcing_functions = environment["forcing_functions"]
    ff_locations      = environment["ff_locations"]
    time_steps        = environment["time_steps"]
    space_steps       = environment["space_steps"]
    dx                = environment["dx"]
    dt                = environment["dt"]

    out = [[]]
    # Nested array:
        # Each top level index corresponds to a particular step in time
        # Each instance in time contains an array for the B field and an array for the E field
        # The B field array is conceptually interleaved in space with the E field.

    init = True

    if init:
        out[0] = init_cond
    else:
        pass

    for n in range(time_steps):
        new_out = []
        new_E_list = []
        new_H_list = []

        if n == (time_steps-1):
            time_boundary = True
        else:
            time_boundary = False

        for i in range(space_steps):
            # Determine if boundary conditions apply
            if (i==0):
                lower_boundary = True
                upper_boundary = False
                solution_space = False
            elif (i==space_steps-1):
                lower_boundary = False
                upper_boundary = True
                solution_space = False
            else:
                solution_space = True
                lower_boundary = False
                upper_boundary = False

            # First, determine the coefficients:
            A = dt/(2*dx*u[i])
            B = 1-((dt*s[i])/(e[i]))
            C = dt/(dx*e[i])

            # Extract the value of the forcing functions:
            for f in ff_locations:
                # Determine if the current point in space is forced
                if f==i:
                    forced            = True
                    forced_value      = forcing_functions[f][n]
                    if time_boundary:
                        next_forced_value = forcing_functions[f][n]
                    else:
                        next_forced_value = forcing_functions[f][n+1]
                else:
                    forced       = False
                    forced_value = None

            # n is discrete time, i is discrete space
            # Define the FD terms:
            if lower_boundary:
                old_right_H = out[n-1][1][i+1]
                new_left_H  = boundary_cond[1][0]
                old_right_E = out[n-1][0][i+1]
                old_E       = boundary_cond[0][0]
            else:
                pass

            if forced:
                old_E       = forced_value
                old_right_H = out[n-1][1][i+1]
                new_left_H  = new_H_list[i-1]
                old_right_E = out[n-1][0][i+1]
            else:
                pass
            
            # If we are in the regular solution space, evaluate the diff eq:
            if solution_space:
                old_right_H = out[n-1][1][i+1]
                new_left_H  = new_H_list[i-1]
                old_right_E = out[n-1][0][i+1]
                old_E       = out[n-1][0][i]

            if upper_boundary == False:
                new_right_H = old_right_H - A * (old_right_E - old_E)
                new_E       = B * old_E - C * ( new_right_H - new_left_H )
            
            if upper_boundary:
                old_right_H = boundary_cond[1][1]
                old_right_E = boundary_cond[0][1]
                new_left_H  = new_H_list[i-1]
                old_E       = out[n-1][0][i]
                new_right_H = boundary_cond[1][1]
                new_E       = B * old_E - C * ( new_right_H - new_left_H )
            else:
                pass

            if forced:
                new_E = next_forced_value
            
            new_E_list.append(new_E)
            new_H_list.append(new_right_H)
        
        new_out.append(new_E_list)
        new_out.append(new_H_list)
        out.append(new_out)
        init = False
            

    return out


    