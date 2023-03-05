import numpy as np
# import matplotlib as plt
import matplotlib.pyplot as plt


def adder(data, times):
    for i in range(1, times + 1):
        new = np.zeros((len(data), 1), dtype=float)
        data = np.append(data, new, axis=1)
    return data


# def bull_bear_power(data, lookback, high, low, close, where):
def bull_bear_power(data, alpha, lookback, high, low, close, where):
    # Adding columns
    data = adder(data, 3)

    # exp average
    data = ema(data, alpha, lookback, close, where)

    # Bull Power
    data[:, where + 1] = data[:, high] - data[:, where]
    # data[:, where + 1] = data[:, high] - data[:, where]+(data[:, high] - data[:, low])

    # Bear Power
    data[:, where + 2] = data[:, low] - data[:, where]

    # Deleting EMA Column
    data = deleter(data, where, 1)

    return data


def deleter(data, index, times):
    for i in range(1, times + 1):
        data = np.delete(data, index, axis=1)
    return data


def jump(data, jump):
    data = data[jump:, ]
    return data


def ma(data, lookback, close, where):
    data = adder(data, 1)

    for i in range(len(data)):

        try:

            data[i, where] = (data[i - lookback + 1:i + 1, close].mean())

        except IndexError:

            pass

    # data = jump(data, lookback)

    return data


def ema(data, alpha, lookback, what, where):
    alpha = alpha / (lookback + 1.0)

    beta = 1 - alpha

    data = ma(data, lookback, what, where)
    data[lookback + 1, where] = (data[lookback + 1, what] * alpha) + (data[lookback, where] * beta)
    for i in range(lookback + 2, len(data)):

        try:

            data[i, where] = (data[i, what] * alpha) + (data[i - 1, where] * beta)

        except IndexError:

            pass

    return data


def indicator_plot_double_bull_bear(data, name='', name_ind='', window=250):

    fig, ax = plt.subplots(2, figsize=(10, 5))
    chosen = data[-window:, ]

    for i in range(len(chosen)):
        ax[0].vlines(x=i, ymin=chosen[i, 2], ymax=chosen[i, 1], color='black', linewidth=1)

    ax[0].grid()
    for i in range(len(chosen)):
        ax[1].vlines(x=i, ymin=0, ymax=chosen[i, 7], color='green', linewidth=1)
        ax[1].vlines(x=i, ymin=chosen[i, 8], ymax=0, color='red', linewidth=1)
        # ax[1].vlines(x=i, ymin=0, ymax=chosen[i, 6], color='green', linewidth=1)
        # ax[1].vlines(x=i, ymin=chosen[i, 7], ymax=0, color='red', linewidth=1)

    ax[1].grid()
    ax[1].axhline(y=0, color='black', linewidth=0.5, linestyle='--')
    plt.show()

