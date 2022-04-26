import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate, signal
import json
from PyQt5.QtWidgets import QApplication, QFileDialog

# Define settings
config_filename = "conf.json"
with open(config_filename, "r") as file:
    conf = json.load(file)

# # Select data file
app = QApplication([])
data_filename = QFileDialog().getOpenFileName(caption="Select data file")[0]
app.quit()

# Read data
flow = np.genfromtxt(data_filename)

# Calculate volume
flow_filtered = signal.savgol_filter(flow, conf["filter_window_length"], conf["filter_order"])
volume = integrate.cumtrapz(flow_filtered, dx=conf["dx"], initial=conf["initial"])

# Plot results
plt.plot(flow, label="Flow")
plt.plot(volume, label="Volume")
plt.legend()
plt.show()
