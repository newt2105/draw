import pandas as pd
import yaml

from common.common import *


"""
    input: 
        Name                    Type            Mean

        + path_raw_file:        string          path of raw file
        + edited_file_path:     string          path of edited file
        + average_data:         list            data needs to processed
        + setname:              dict            set of name
        + order:                list            order of name in chart
        + convert_to_float:     list            data needs to converted to float
    output:
        + path_output_file:          string
    summary: this file convert raw file to new file with proccessed data
"""
def process_data_by_setname(

    average_data:       list,
    column_set:          str,
    setname:            list, 
    order:              list, 
    convert_to_float:   list,
    raw_file:           str = RAW_FILE , 
    edited_file_path:   str = OUT_PUTFILE, 
    ):
    # read from raw file .csv
    processed_data = pd.read_csv(raw_file)


    # convert data type to float
    processed_data[convert_to_float] = processed_data[convert_to_float].astype(float)

    # divide the corresponding coefficient
    for setname, factor in setname.items():
        mask = processed_data[column_set] == setname
        processed_data.loc[mask, average_data] /= factor

    # determine the order of setname
    setname_order = pd.CategoricalDtype(categories=order, ordered=True)
    processed_data[column_set] = processed_data[column_set].astype(setname_order)

    # sort data frame by order of setname
    processed_data.sort_values(by=column_set, inplace=True)

    # Save result in new file
    processed_data.to_csv(edited_file_path, index=False)
    print("done")

def Main():
    # read config and common file
    with open('./config/presolve/config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    
    # main process
    process_data_by_setname(
        average_data =      config['average_data'] , 
        column_set =        config['column_set'], 
        setname =           config['setname'], 
        order =             config['order'] , 
        convert_to_float =  config['convert_to_float'] 
        )
