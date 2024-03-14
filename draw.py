import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

pd.set_option('future.no_silent_downcasting', True)

def read_data(file_path):
    return pd.read_csv(file_path)

def filter_solver(df, solver):
    return df[df["solvername"] == solver]

def create_comparison_plot(ax, data, labels, df,  colours, edgecolors, markers=None):
    
    bars = []
    bar_width = 0.15
    index = np.arange(len(data[0]))

    if markers is None:
        markers = ['/', '.', '']  # customize the markers as needed

    for i, dataset in enumerate(data):
        bars.append(ax.bar(index + i * (bar_width+0.02), dataset, width=bar_width, label=labels[i], hatch=markers[i], color = colours[i], edgecolor = edgecolors[i]))

    ax.set_xticks(index + (bar_width + 0.015) * (len(data) - 1) / 2 )
    df['setname'] = df['setname'].replace({'DUMMY': 100, 'DUMMY2': 200, 'DUMMY04': 40, 'DUMMY07': 70})
    ax.set_xticklabels(df["setname"].unique())

        
    
    # ax.legend(fontsize='x-large', loc = "upper right", fancybox=True)


    return bars

def add_values(bars, ax):
    for bar in bars:
        for b in bar:
            yval = b.get_height()
            ax.text(b.get_x() + b.get_width()/2, yval, f'{round(yval, 1):.1f}', ha='center', va='bottom')

def save_plot(fig, filename, folder='fig'):
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    filepath = os.path.join(folder, filename)
    fig.tight_layout()
    fig.savefig(filepath)
    print(f"Figure saved as {filepath}")



def plot_and_save_comparison(df,y_name,data, labels,  filename, ylim_bottom = None, ylim_top = None):
    plt.rc('text', usetex=True)
    plt.rc('font', family='sans-serif')
    # plt.rc('font', size='x-large') 

    setname_order = ['DUMMY04', 'DUMMY07', 'DUMMY', 'DUMMY2']
    df['setname'] = pd.Categorical(df['setname'], categories=setname_order, ordered=True)
    df = df.sort_values('setname')

    # Filter data for each solver
    ilp_df = filter_solver(df, "ILP_GUROBI")
    gr_df = filter_solver(df, "GREEDY")
    ql_df = filter_solver(df, "QL_DUMMY")

    # Create subplot
    fig, ax = plt.subplots(figsize=(8, 6))
        
    # Colors for different bars
    colors = ["w", "w", "w"]
    edgecolors = ["black", "green", "black"]

    # Comparison plot
    comparison_data = [ilp_df.groupby("setname")[data].mean(),
                       ql_df.groupby("setname")[data].mean(),
                       gr_df.groupby("setname")[data].mean()]
    comparison_bars = create_comparison_plot(ax, comparison_data, labels,  df, colors, edgecolors)
    # add_values(comparison_bars, ax)
    if data == 'runtime':
        # add_values(comparison_bars, ax)
        ax.legend(fontsize=20, loc = "upper left", fancybox=True)
    
    if data == 'usedlinksrate':
        ax.legend(fontsize=17, loc = "lower left", fancybox=True)

    # Set ylim to increase space above the plot if ylim_top is provided
    if ylim_top is not None:
        ax.set_ylim(ylim_bottom, top=ylim_top)  

    if data == 'usedlinksrate':
        ax.set_yticks([0, 5, 10, 15]) 

    # Set ylabel for each plot
    if data == 'runtime':
        ax.set_ylabel('Runtime (s)', fontsize=25)
        ax.set_yscale('log')
    else:
        ax.set_ylabel(f'{y_name} ', fontsize=25)

    # Draw grid lines
    ax.set_axisbelow(True)
    ax.grid(True, linestyle='--', alpha=0.7)

    # Set xlabel
    ax.set_xlabel('Number of slices', fontsize=25)
    ax.tick_params(axis='both', which='major', labelsize=25)
    # Add numbers at the origin
    # ax.annotate( xy=(0, 0), xytext=(0.02, 0.02), textcoords='axes fraction', ha='left', va='bottom', fontsize='x-large')

    # Save the figure
  
    save_plot(fig, f'{filename}.pdf')

    # plt.show()

if __name__ == "__main__":
    df = read_data('ten_file_processed3.csv')
    # Plot and save comparison for "objvalue"
    plot_and_save_comparison(df,y_name = "Acceptance rate" ,data = "objvalue", labels = ["ILP-SE", "QL-SE", "Greedy-SE"], filename= "objvalue_comparison", ylim_top= 1.05)
    plot_and_save_comparison(df,y_name = "Run time" ,data = "runtime", labels = ["ILP-SE", "QL-SE", "Greedy-SE"],  filename="runtime_comparison")
    plot_and_save_comparison(df,y_name = "Used links per slices" ,data = "usedlinksrate", labels = ["ILP-SE", "QL-SE", "Greedy-SE"],  filename="usedlinkscount_comparison",  ylim_top= 15)