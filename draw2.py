import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import yaml

def filterSolver(df, solver):
    return df[df["solvername"] == solver]

def createComparisonPlot(ax, data, labels, df, colours, edgecolors, replace, markers=None):
    bars = []
    bar_width = 0.15
    index = np.arange(len(data[0]))

    if markers is None:
        markers = ['/', '.', '']  # customize the markers as needed

    for i, dataset in enumerate(data):
        bars.append(ax.bar(index + i * (bar_width+0.02), dataset, width=bar_width, label=labels[i], hatch=markers[i], color=colours[i], edgecolor=edgecolors[i]))

    ax.set_xticks(index + (bar_width + 0.015) * (len(data) - 1) / 2 )
    df['setname'] = df['setname'].replace(replace)
    ax.set_xticklabels(df["setname"].unique())
    ax.legend(fontsize='x-large', loc="upper right", fancybox=True)
    return bars

def addValues(bars, ax):
    for bar in bars:
        for b in bar:
            yval = b.get_height()
            ax.text(b.get_x() + b.get_width()/2, yval, f'{round(yval, 1):.1f}', ha='center', va='bottom')

def savePlot(fig, filename, folder='fig'):
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    filepath = os.path.join(folder, filename)
    fig.tight_layout()
    fig.savefig(filepath)
    print(f"Figure saved as {filepath}")

def plotAndSaveComparison(df, order, solver, y_name, data, labels, replace, filename, ylim_bottom=None, ylim_top=None, runtime = False):
    plt.rc('text', usetex=True)
    plt.rc('font', family='sans-serif')

    df['setname'] = pd.Categorical(df['setname'], categories=order, ordered=True)
    df = df.sort_values('setname')

    comparison_data = []

    for i in range(len(solver)):
        # Filter data for each solver
        solver_df = filterSolver(df, solver[i])
        comparison_data.append(solver_df.groupby("setname")[data].mean())

    # Create subplot
    fig, ax = plt.subplots(figsize=(8, 6))
        
    # Colors for different bars
    colors = ["w", "w", "w"]
    edgecolors = ["black", "green", "black"]

    # Comparison plot
    comparison_bars = createComparisonPlot(ax, comparison_data, labels, df, colors, edgecolors, replace)

    if ylim_top is not None:
        ax.set_ylim(ylim_bottom, top=ylim_top)  

    if runtime == True:
        ax.legend(fontsize=20, loc="upper left", fancybox=True)
        ax.set_ylabel('Runtime (s)', fontsize=25)
        ax.set_yscale('log')
    else:
        ax.set_ylabel(f'{y_name} ', fontsize=25)

    ax.set_axisbelow(True)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.set_xlabel('Number of slices', fontsize=25)
    ax.tick_params(axis='both', which='major', labelsize=25)

    savePlot(fig, f'{filename}.png')

def Main():
    with open('./config/draw/config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    df = pd.read_csv(config['data_file']) # read in put file

    for plot_config in config['plot_configs']:
        plotAndSaveComparison(
            df,
            config['order'], # order of set name in chart
            config['solver'], # name of solver
            y_name=plot_config['y_name'], 
            data=plot_config['data'], # type of data
            labels=config['labels'], # legend order
            replace=config['replace'], 
            filename=plot_config['filename'], # name of output file
            ylim_top=plot_config.get('ylim_top'), # limit of y axis
            runtime=plot_config.get('runtime') # check if it is runtime or not
        )
