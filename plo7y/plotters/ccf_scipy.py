from scipy import signal
import numpy as np
import matplotlib.pyplot as plt


def plot(sig, sig_2, *args, saveFigPath):
    corr = signal.correlate(sig_2, np.ones(128), mode='same') / 128
    clock = np.arange(64, len(sig), 128)
    fig, (ax_orig, ax_noise, ax_corr) = plt.subplots(3, 1, sharex=True)
    ax_orig.plot(sig)
    ax_orig.plot(clock, sig[clock], 'ro')
    ax_orig.set_title('Original signal')
    ax_noise.plot(sig_2)
    ax_noise.set_title('Signal with noise')
    ax_corr.plot(corr)
    ax_corr.plot(clock, corr[clock], 'ro')
    ax_corr.axhline(0.5, ls=':')
    ax_corr.set_title('Cross-correlated with rectangular pulse')
    ax_orig.margins(0, 0.1)
    fig.tight_layout()
    plt.savefig(saveFigPath)
