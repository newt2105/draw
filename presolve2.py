import pandas as pd
import yaml

"""
    input:
        + path_raw_file:        string
        + edited_file_path:     string
        + average_data:         list
        + setname:              dic
        + order:                list
        + convert_to_float:     list
    output:
        + path_output_file:          string
    summary: this file convert raw file to new file with proccessed data
"""

def process_data_by_setname(
    raw_file: str, 
    edited_file_path: str, 
    average_data: list,
    columname: str,
    setname: list, 
    order: list, 
    convert_to_float: list
    ):
    # read from raw file .csv
    processed_data = pd.read_csv(raw_file)


    # convert data type to float
    processed_data[convert_to_float] = processed_data[convert_to_float].astype(float)

    # divide the corresponding coefficient
    for setname, factor in setname.items():
        mask = processed_data[columname] == setname
        processed_data.loc[mask, average_data] /= factor

    # determine the order of setname
    setname_order = pd.CategoricalDtype(categories=order, ordered=True)
    processed_data[columname] = processed_data[columname].astype(setname_order)

    # sort data frame by order of setname
    processed_data.sort_values(by=columname, inplace=True)

    # Save result in new file
    processed_data.to_csv(edited_file_path, index=False)
    print("done")

def Main():
    # read config and common file
    with open('./config/presolve/config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    with open('./common/common.yaml', 'r') as f:
        common = yaml.safe_load(f)

    file_path = common['RAW_FILE'] # original file
    output_file_path = common['OUT_PUTFILE'] # output file
    columname = config['columname']
    average_data = config['average_data'] # data needs to be averaged
    setname_mapping = config['setname'] # set name
    order = config['order'] # order of set name in chart
    convert_to_float = config['convert_to_float'] # data needs to converted to float
    
    # main process
    process_data_by_setname(
        file_path, 
        output_file_path, 
        average_data, 
        columname, 
        setname_mapping, 
        order, 
        convert_to_float
        )
