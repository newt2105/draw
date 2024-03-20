
import numpy as np

def createComparisonPlot(ax, data, column_set, labels, df, colours, edgecolors, replace, markers=None):
    bars = []
    bar_width = 0.15
    index = np.arange(len(data[0]))

    if markers is None:
        markers = ['/', '.', '']  # customize the markers as needed

    for i, dataset in enumerate(data):
        bars.append(ax.bar(index + i * (bar_width+0.02), dataset, width=bar_width, label=labels[i], hatch=markers[i], color=colours[i], edgecolor=edgecolors[i]))

    ax.set_xticks(index + (bar_width + 0.015) * (len(data) - 1) / 2 )
    df[column_set] = df[column_set].replace(replace)
    ax.set_xticklabels(df[column_set].unique())
    ax.legend(fontsize='x-large', loc="upper right", fancybox=True)
    return bars