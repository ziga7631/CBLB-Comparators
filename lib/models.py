# models as used in https://doi.org/10.1016/j.compbiomed.2020.104109 
# this code is adapted version of the code available at https://github.com/mmoskon/CBLBs/
import numpy as np

# a model of inverter
def not_cell(state, params):
    L_X, x, y = state
    delta_L, gamma_L_X, n_y, theta_L_X, eta_x, omega_x, m_x, delta_x, rho_x = params

    f = gamma_L_X * (y ** n_y)/(1 + (theta_L_X*y)**n_y )
    dL_X_dt = (f - delta_L * L_X)

    dx_dt = (eta_x * (1/(1+ (omega_x*L_X)**m_x))) - (delta_x * x) - rho_x * x # rho ... increased degradation rate

    return dL_X_dt, dx_dt


# a model of driver
def yes_cell(state, params):
    x, y = state
    gamma_x, n_y, theta_x, delta_x, rho_x = params

    dx_dt = gamma_x * (y ** n_y)/(1 + (theta_x*y)**n_y ) - (delta_x * x) - rho_x * x # rho ... increased degradation rate
    
    return dx_dt


# L_A ... intermediate
# a ... out
# b ... in
def not_cell_wrapper(state, params):
    L_A, a, b = state
    
    state_A = L_A, a, b
    params_A = params

    return not_cell(state_A, params_A)


# a ... out
# b ... in
def yes_cell_wrapper(state, params):
    a, b = state

    state_A = a, b
    params_A = params

    return yes_cell(state_A, params_A)


def not_model(T, state, params):
    L_A, a, b = state

    delta_L, gamma_L_A, n_b, theta_L_A, eta_a, omega_a, m_a, delta_a, delta_b, rho_a, rho_b = params

    state_not = L_A, a, b
    params_not = delta_L, gamma_L_A, n_b, theta_L_A, eta_a, omega_a, m_a, delta_a, rho_a
    dL_A_dt, da_dt = not_cell_wrapper(state_not, params_not)
    
    db_dt = 0

    return np.array([dL_A_dt, da_dt, db_dt])


def yes_model(T, state, params):
    a, b = state
    
    gamma_a, n_b, theta_a, delta_a, delta_b, rho_a, rho_b = params

    state_yes = a, b
    params_yes = gamma_a, n_b, theta_a, delta_a, rho_a
    da_dt = yes_cell_wrapper(state_yes, params_yes)
    db_dt = 0 

    return np.array([da_dt, db_dt])


# A v NEG(B)
def yes_not_or(state, params):
    # Load params
    delta_L, gamma_A, n_b, theta_A, eta_a, omega_a, m_a, delta_a, rho_a = params
    # Assign params
    params_yes = gamma_A, n_b, theta_A, delta_a, rho_a
    params_not = delta_L, gamma_A, n_b, theta_A, eta_a, omega_a, m_a, delta_a, rho_a
    # Read the state
    L_I, a, b, I = state
    # Prepare new states
    state_yes = I, a
    state_not = L_I, I, b
    # Observe change in a
    dI = yes_cell_wrapper(state_yes, params_yes)
    # Observe change in b
    dL_B, dI1 = not_cell_wrapper(state_not, params_not)
    dI += dI1
    # Return
    return dL_B, dI


# A v B
def yes_yes_or(state, params):
    # Load params
    delta_L, gamma_A, n_b, theta_A, eta_a, omega_a, m_a, delta_a, rho_a = params
    # Assign params
    params_yes = gamma_A, n_b, theta_A, delta_a, rho_a
    # Read the state
    a, b, I = state
    # Prepare new states
    state_one = I, a
    state_two = I, b
    # Observe change in a
    dI = yes_cell_wrapper(state_one, params_yes)
    # Observe change in b
    dI += yes_cell_wrapper(state_two, params_yes)
    # Return
    return dI

# NEG(A) v NEG(B)
def not_not_or(state, params):
    # Load params
    delta_L, gamma_A, n_b, theta_A, eta_a, omega_a, m_a, delta_a, rho_a = params
    # Assign params
    params_not = delta_L, gamma_A, n_b, theta_A, eta_a, omega_a, m_a, delta_a, rho_a
    # Read the state
    L_I, a, b, I = state
    # Prepare new states
    # TODO Check if L_I used both times is OK
    state_one = L_I, I, a
    state_two = L_I, I, b
    # Observe change in a
    dL_I, dI = not_cell_wrapper(state_one, params_not)
    # Observe change in b
    dL_Temp, dTemp = not_cell_wrapper(state_two, params_not)
    # Sum
    dL_I += dL_Temp
    dI += dTemp
    # Return
    return dL_I, dI


# NEG(A) v NEG(B)
def probably_wrong_not_not_or(state, params):
    # Load params
    delta_L, gamma_A, n_b, theta_A, eta_a, omega_a, m_a, delta_a, rho_a = params
    # Assign params
    params_not = delta_L, gamma_A, n_b, theta_A, eta_a, omega_a, m_a, delta_a, rho_a
    # Read the state
    L_A, L_B, a, b, I = state
    # Prepare new states
    # TODO I think L_ should always be dependant on output - in our case I (see not_not_or)
    state_one = L_A, I, a
    state_two = L_B, I, b
    # Observe change in a
    dL_A, dI = not_cell_wrapper(state_one, params_not)
    # Observe change in b
    dL_B, dTemp = not_cell_wrapper(state_two, params_not)
    # Sum
    dI += dTemp
    # Return
    return dL_A, dL_B, dI