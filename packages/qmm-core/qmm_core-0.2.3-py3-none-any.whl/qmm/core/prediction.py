import numpy as np
import sympy as sp
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def table_of_predictions(M, t1=0.8, t2=1, index=None, columns=None):
    if isinstance(M, sp.Matrix):
        M = sp.matrix2numpy(M, dtype=float)
    conditions = [
        (lambda x: x == sp.nan, "0"),
        (lambda x: x >= t2, "+"),
        (lambda x: x >= t1 and x < t2, "(+)"),
        (lambda x: x > -t1 and x < t1, "?"),
        (lambda x: x > -t2 and x <= -t1, "(\u2212)"),
        (lambda x: x <= -t2, "\u2212"),
    ]

    predictions = np.empty(M.shape, dtype=object)
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            value = M[i, j]
            predictions[i, j] = next(
                (val for cond, val in conditions if cond(value)), "0"
            )
    return pd.DataFrame(predictions, index=index, columns=columns)


def compare_predictions(M1, M2):
    if not M1.index.equals(M2.index) or not M1.columns.equals(M2.columns):
        raise ValueError("M1 and M2 must have the same index and columns")
    combined = np.vectorize(lambda x, y: x if x == y else f"{x}, {y}")(
        M1.values, M2.values
    )
    return pd.DataFrame(combined, index=M1.index, columns=M1.columns)


def create_plot(data, **kwargs):
    plt.rcParams.update(
        {
            "xtick.top": True,
            "xtick.bottom": False,
            "xtick.labeltop": True,
            "xtick.labelbottom": False,
            "xtick.major.width": 0.5,
            "ytick.major.width": 0.5,
            "xtick.major.size": 3,
            "ytick.major.size": 3,
            "xtick.minor.size": 1.5,
            "ytick.minor.size": 1.5,
        }
    )
    args = {
        "annot": True,
        "linewidths": 0.75,
        "linecolor": "white",
        "cbar": False,
        "cmap": None,
    }
    args.update(kwargs)
    figsize = args.pop("figsize", None)
    if figsize:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig, ax = plt.subplots()
    sns.heatmap(data, ax=ax, **args)
    plt.setp(ax.get_xticklabels(), rotation=0, ha="center")
    plt.setp(ax.get_yticklabels(), rotation=0, ha="right")
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_color("white")
        spine.set_linewidth(0.5)
    return fig, ax
