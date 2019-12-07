from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm


def prep_dataframes(df1, df2):
    # TODO: do a more throrough check
    # print("ndims: {}, {}".format(df1.ndim, df2.ndim))
    if df1.ndim == 2:
        df1 = df1.squeeze().to_numpy()
    if df2.ndim == 2:
        df2 = df2.squeeze().to_numpy()

    # if STILL ndim == 2 (ie dataframe w/ index loaded w/o using index_col)
    # rm index column inserted by pd.to_csv:
    if df1.ndim == 2:
        df1 = df1.squeeze().to_numpy()[1, :]
    if df2.ndim == 2:
        df2 = df2.squeeze().to_numpy()[1, :]

    return df1, df2

def plot(sig, sig_2, saveFigPath=None):
    sig, sig_2 = prep_dataframes(sig, sig_2)
    sig_len = 128
    # signal_len = len(sig)
    corr = signal.correlate(sig_2, np.ones(sig_len), mode='same') / sig_len
    # corr = sm.tsa.ccf(sig.values.squeeze(), sig_2.values.squeeze())
    # clock = np.arange(sig_len/2, len(sig), sig_len)
    fig, (ax_orig, ax_noise, ax_corr) = plt.subplots(3, 1, sharex=True)
    ax_orig.plot(sig)
    # clock = np.arange(64, len(sig), sig_len)
    # ax_orig.plot(clock, sig[clock], 'ro')
    ax_orig.set_title('Signal 1')
    ax_noise.plot(sig_2)
    ax_noise.set_title('Signal 2')
    ax_corr.plot(corr)
    # ax_corr.plot(clock, corr[clock], 'ro')
    ax_corr.axhline(0.5, ls=':')
    ax_corr.set_title('Cross-correlated signals')
    ax_orig.margins(0, 0.1)
    fig.tight_layout()
    if saveFigPath is None:
        plt.show()
    else:
        plt.savefig(saveFigPath)
