import numpy as np
import matplotlib.pyplot as plt


def main():
    output_filename = "data.csv"
    amplitude = 10
    frequency = 1
    offset = 0.1
    noise_amplitude = .5
    signal_duration = 1
    prefix_duration = 0.5
    sample_freq = 100

    signal = create_sample_data(amplitude, frequency, offset, noise_amplitude,
                                signal_duration, prefix_duration, sample_freq)

    np.savetxt(output_filename, signal[:, 1], header="Data")

    plt.plot(signal[:, 0], signal[:, 1])
    plt.show()


def create_sample_data(amplitude, frequency, offset, noise_amplitude, signal_duration, prefix_duration, sample_freq):

    time = np.linspace(0, signal_duration, int(signal_duration*sample_freq))
    sin = np.sin(time * frequency * 2 * np.pi)
    noise = np.random.normal(0, 1, int(signal_duration*sample_freq))

    prefix_time = np.linspace(0, prefix_duration, int(prefix_duration*sample_freq))
    prefix_noise = np.random.normal(0, 1, int(prefix_duration*sample_freq))

    signal = sin * amplitude \
             + noise * noise_amplitude \
             + offset
    prefix_signal = prefix_noise * noise_amplitude\
                    + offset

    time = np.append(prefix_time, time + (prefix_time[-1] if len(prefix_time >0) else 0))
    signal = np.append(prefix_signal, signal)

    return np.array((time, signal)).T


if __name__ == "__main__":
    main()
