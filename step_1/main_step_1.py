import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate, signal

# Define settings
data_filename = "../data.csv"
filter_window_length = 20
filter_order = 2
dx = 0.01
initial = 0

# Read data
flow = np.genfromtxt(data_filename)

# Calculate volume
flow_filtered = signal.savgol_filter(flow, filter_window_length, filter_order)
volume = integrate.cumtrapz(flow_filtered, dx=dx, initial=initial)

# Plot results
plt.plot(flow, label="Flow")
plt.plot(volume, label="Volume")
plt.legend()
plt.show()
