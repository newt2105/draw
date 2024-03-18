import pandas as pd
import yaml

"""
    input:
        + raw_file:             string
        + edited_file_path:     string
        + average_data:         list
        + setname:              dictionary
        + order:                list
        + convert_to_float:     list
    output:
        + output_file:          string
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
    # Đọc dữ liệu từ file CSV
    df = pd.read_csv(raw_file)

    # Tạo một bản sao của DataFrame để tránh ảnh hưởng đến dữ liệu gốc
    processed_data = df.copy()

    # Chuyển đổi kiểu dữ liệu của các cột sang float
    processed_data[convert_to_float] = processed_data[convert_to_float].astype(float)

    # Duyệt qua từng dòng và áp dụng hệ số chia tương ứng
    for setname, factor in setname.items():
        mask = processed_data[columname] == setname
        processed_data.loc[mask, average_data] /= factor

    # Xác định thứ tự ưu tiên của các giá trị setname
    setname_order = pd.CategoricalDtype(categories=order, ordered=True)
    processed_data[columname] = processed_data[columname].astype(setname_order)

    # Sắp xếp DataFrame theo thứ tự setname
    processed_data.sort_values(by=columname, inplace=True)

    # Lưu kết quả vào file CSV mới
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
