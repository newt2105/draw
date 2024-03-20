import os
import yaml

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from helper.createPlot import createComparisonPlot
from helper.save import savePlot
from common.common import *


"""
    input:
    Name            Type            Mean?
    + df:           dataframe       dataframe
    + order:        list            order of name in chart
    + solver:       list            name of solver
    + y_name:       string          name of y_column
    + data:         string          name of data
    + label:        list            name of legend
    + replace:      dict            
    + file name:    string          output file name
    + fontsize:     float           
    + alpha:        float
    + labelsize:    float
    + yscale:       string          type of y culumn
    + ylim_top:     float           maximum of y column

    output:          picture

    summary: this function is used to draw a picture from edited file
"""
def plotAndSaveComparison(
        df:             pd.DataFrame,
        column_set:     str,
        column_solver:  str,
        order:          list, 
        solver:         list, 
        y_name:         str,  
        data:           str,    
        labels:         list, 
        replace:        dict,  
        yscale:         str, 
        filename:       str,
        fontsizelegend: str,
        loc:            str,
        fancybox:       bool = FANCYBOX,
        colors:         list = COLORS,
        edgecolors:     list = EDGECOLORS,
        linestyle:      list = LINESTYLE,
        fontsize:       float = FONT_SIZE,
        family:         str   = FAMILY,
        alpha:          float = ALPHA,
        labelsize:      float = LABELSIZE,
        ylim_bottom:    float = None, 
        ylim_top:       float = None,
):
    plt.rc('text', usetex=True)
    plt.rc('font', family=family)

    df[column_set] = pd.Categorical(df[column_set], categories=order, ordered=True)
    df = df.sort_values(column_set)

    comparison_data = []
    for sol in solver:
        solver_df = df[df["solvername"] == sol]
        comparison_data.append(solver_df.groupby(column_set)[data].mean())

    # Create subplot
    fig, ax = plt.subplots(figsize=(8, 6))
        

    # Comparison plot
    createComparisonPlot(ax, comparison_data, column_set, labels, df, colors, edgecolors, replace)

    ax.legend(fontsize=fontsizelegend, loc=loc, fancybox=fancybox)

    if ylim_top is not None:
        ax.set_ylim(ylim_bottom, top=ylim_top)  

    ax.set_ylabel(f'{y_name} ', fontsize=fontsize) 
    ax.set_yscale(yscale)

    ax.set_axisbelow(True)
    ax.grid(True, linestyle=linestyle, alpha=alpha)
    ax.set_xlabel('Number of slices', fontsize=fontsize)
    ax.tick_params(axis='both', which='major', labelsize=labelsize)

    savePlot(fig, f'{filename}.png')

def Main():
    with open('./config/draw/config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    df = pd.read_csv(EDITED_FILE ) # read in put file
    # print(df)

    for plot_config in config['plot_configs']:
        plotAndSaveComparison(
            df              = df,
            column_set      = config['column_set'],
            column_solver   = config['column_solver'],
            order           = config['order'], 
            solver          = config['solver'], 
            y_name          = plot_config['y_name'], 
            data            = plot_config['data'], 
            labels          = config['labels'], 
            replace         = config['replace'], 
            filename        = plot_config['filename'], 
            fontsizelegend  = plot_config['fontsize'],
            loc             = plot_config['loc'],
            yscale          = plot_config.get('yscale'), 
            ylim_top        = plot_config.get('ylim_top'), 
        )
