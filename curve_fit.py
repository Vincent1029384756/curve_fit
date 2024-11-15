# Curve fit using the scipy curve fit function

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Define the spring-damper model
def spring_damper_model(t, x0, v0, omega_n, zeta, y_offset):
    omega_d = omega_n * np.sqrt(1 - zeta**2)
    oscillation = (
        np.exp(-zeta * omega_n * t) *
        (x0 * np.cos(omega_d * t) + (v0 + zeta * omega_n * x0) / omega_d * np.sin(omega_d * t))
    )
    return oscillation + y_offset

# Step 1: Import data from CSV
data = pd.read_csv('/home/wen-gu/Documents/439_lab/csv/sample2.csv')
time = data['time [s]'].values
displacement = data['cy [mm]'].values


x0_guess = displacement[0]
v0_guess = (displacement[1] - displacement[0]) / (time[1] - time[0])
omega_n_guess = 2 * np.pi / (time[np.argmax(displacement)] - time[np.argmin(displacement)])  # Approximate natural frequency
zeta_guess = 0.1  # Start with small damping
offset_guess = np.mean(displacement[-10:])  # Use the last 10 points to estimate offset

initial_guess = [x0_guess, v0_guess, omega_n_guess, zeta_guess, offset_guess]

# Fit the model
popt, pcov = curve_fit(spring_damper_model, time, displacement, p0=initial_guess)

# Extract fitted parameters
fitted_x0, fitted_v0, fitted_omega_n, fitted_zeta, fitted_y_offset = popt
print(f"Fitted x0: {fitted_x0}")
print(f"Fitted v0: {fitted_v0}")
print(f"Fitted omega_n: {fitted_omega_n}")
print(f"Fitted zeta: {fitted_zeta}")
print(f"Fitted y_offset: {fitted_y_offset}")

# Calculates k and c
alpha = 0.3 # portion of the mass being oscillated
mass = 0.0263 #kg
m_eff = mass*alpha #kg, effective mass
k = (fitted_omega_n**2)*m_eff #N/m
c = 2*fitted_zeta*fitted_omega_n*m_eff

# Step 5: Plot results
plt.figure()
plt.plot(time, displacement, 'b.', label='Data')
plt.plot(time, spring_damper_model(time, *popt), 'r-', label='Fitted Model')
plt.legend()
plt.xlabel('Time (s)')
plt.ylabel('Displacement (m)')
plt.title('Spring-Damper Model Curve Fitting E-30')
plt.figtext(0.5, 0.01, f"k = {k: .2f} N/m, c = {c: .4f} N*s/m", 
            fontsize=10, ha='center')
plt.show()
