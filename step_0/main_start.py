import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate, signal

# Read data
flow = np.genfromtxt("../data.csv")

# Calculate volume
flow_filtered = signal.savgol_filter(flow, 20, 2)
volume = integrate.cumtrapz(flow_filtered, dx=0.01, initial=0)

# Plot results
plt.plot(flow, label="Flow")
plt.plot(volume, label="Volume")
plt.legend()
plt.show()
