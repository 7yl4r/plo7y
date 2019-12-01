"""
Generates test_data/generated/ files.
"""
import numpy as np
import pandas as pd

DIRPATH = "./test_data/generated/"


def generate_test_data():
    _get_testdata_out_of_phase_sines()

    _get_testdata_binary_and_noise()


def _get_testdata_out_of_phase_sines():
    print("creating example covariance data.")
    np.random.seed(0)
    x_0 = -10
    x_f = 10
    dx = 200
    x = np.linspace(x_0, x_f, dx)
    y1 = np.sin(x+0) + np.random.normal(-0.1, 0.1, dx)
    y2 = np.sin(x-1) + np.random.normal(-0.1, 0.1, dx)
    # # TODO: output this plot somewhere...
    # plt.plot(x, y1)
    # plt.plot(x, y2)
    # plt.show()
    # plt.savefig(get_test_output_path(__file__, "sample_data"))
    # plt.clf()
    x = pd.DataFrame(x)
    dta = pd.DataFrame(y1)  # [x, y1, y2]  # TODO dataframe?
    exog = pd.DataFrame(y2)
    x.to_csv(DIRPATH + "linspace_x.csv")
    dta.to_csv(DIRPATH + "sine_1.csv")
    exog.to_csv(DIRPATH + "sine_2.csv")
    return x, dta, exog


def _get_testdata_noisy_sines():
    np.random.seed(0)
    # npts = 500
    x = np.linspace(0, 50, 500)

    npts = len(x)
    y1 = 5 * np.sin(x/2) + np.random.randn(npts)
    # y2 = 5 * np.cos(x/2) + np.random.randn(npts)
    y2 = 5 * np.sin(x/2) + np.random.randn(npts)
    return pd.DataFrame(x), pd.DataFrame(y1), pd.DataFrame(y2)


def _get_testdata_binary_and_noise():
    np.random.seed(0)
    sig = np.repeat([0., 1., 1., 0., 1., 0., 0., 1.], 128)
    sig_noise = sig + np.random.randn(len(sig))

    sig = pd.DataFrame(sig)
    sig_noise = pd.DataFrame(sig_noise)
    sig.to_csv(
        DIRPATH + "timeseries_binary_signal.csv"
    )
    sig_noise.to_csv(
        DIRPATH + "timeseries_binary_signal_noisy.csv"
    )

    return sig, sig_noise

if __name__ == "__main__":
    # TODO: generate data & insert into csv file
    pass
