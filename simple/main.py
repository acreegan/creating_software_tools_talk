import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate
import scipy.signal


def main():
    # Set config
    data_filename = "../data.csv"
    dx = 0.01
    filt_window_length = 20
    filt_polyorder = 2

    # Read data
    flow = np.genfromtxt(data_filename)

    # Calculate volume
    flow_filtered = scipy.signal.savgol_filter(flow, filt_window_length, filt_polyorder)
    volume = calculate_volume(flow_filtered, dx)

    # Plot results
    plt.plot(flow, label="Flow")
    plt.plot(volume, label="Volume")
    plt.legend()
    plt.show()


def calculate_volume(flow, dx):
    volume = scipy.integrate.cumtrapz(flow, dx=dx, initial=0)
    return volume


if __name__ == "__main__":
    main()
