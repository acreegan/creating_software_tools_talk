import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate
import scipy.signal
import os
from pathlib import Path


def main():
    # Set config
    data_filename = "data.csv"
    output_directory = "output"
    output_suffix = "_volume.csv"
    filt_window_length = 20
    filt_polyorder = 2

    # Read data
    data = np.genfromtxt(data_filename, delimiter=",", skip_header=True)
    time, flow = data[:, 0], data[:, 1]

    # Calculate volume
    flow_filtered = scipy.signal.savgol_filter(flow, filt_window_length, filt_polyorder)
    volume = calculate_volume(flow_filtered, time)
    data = np.column_stack([data, volume.T])

    # Plot results
    fig, ax = plt.subplots()
    ax.plot(time, flow, label="Flow")
    ax.plot(time, flow_filtered, label="Flow Filtered")
    ax.plot(time, volume, label="Volume")
    ax.legend()
    ax.set_title("Flow and Calculated Volume")
    plt.show()

    # Save results
    if not os.path.exists(output_directory):
        os.mkdir(output_directory)
    output_filename = Path(data_filename).stem + output_suffix
    np.savetxt(f"{output_directory}/{output_filename}", data, delimiter=",", header="Time, Flow, Volume", comments="")


def calculate_volume(flow, time):
    volume = scipy.integrate.cumtrapz(flow, time, initial=0)
    return volume


if __name__ == "__main__":
    main()
