import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate, signal
import json
from tkinter import Tk
from tkinter.filedialog import askopenfilename


def main():
    # Define settings
    config_filename = "conf.json"
    with open(config_filename, "r") as file:
        conf = json.load(file)

    # # Select data file
    Tk().withdraw()
    data_filename = askopenfilename(title="Select data file")
    Tk().destroy()

    # Read data
    flow = np.genfromtxt(data_filename)

    # Calculate volume
    volume = calculate_volume(flow, dx=conf["dx"], initial=conf["initial"],
                              filter_window_length=conf["filter_window_length"], filter_order=conf["filter_order"])

    # Plot results
    plt.plot(flow, label="Flow")
    plt.plot(volume, label="Volume")
    plt.legend()
    plt.show()


def calculate_volume(flow, dx, initial, filter_window_length=None, filter_order=None):
    if filter_window_length is not None and filter_order is not None:
        flow_filtered = signal.savgol_filter(flow, filter_window_length, filter_order)
    else:
        flow_filtered = flow
    volume = integrate.cumulative_trapezoid(flow_filtered, dx=dx, initial=initial)
    return volume


if __name__ == "__main__":
    main()
