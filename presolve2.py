import pandas as pd
import yaml

def process_data_by_setname(file_path, output_file_path, setname_mapping, order, convert_to_float):
    # Đọc dữ liệu từ file CSV
    df = pd.read_csv(file_path)

    # Tạo một bản sao của DataFrame để tránh ảnh hưởng đến dữ liệu gốc
    processed_data = df.copy()

    # Chuyển đổi kiểu dữ liệu của các cột sang float
    processed_data[convert_to_float] = processed_data[convert_to_float].astype(float)

    # Duyệt qua từng dòng và áp dụng hệ số chia tương ứng
    for setname, factor in setname_mapping.items():
        mask = processed_data['setname'] == setname
        processed_data.loc[mask, ['objvalue']] /= factor

    # Xác định thứ tự ưu tiên của các giá trị setname
    setname_order = pd.CategoricalDtype(categories=order, ordered=True)
    processed_data['setname'] = processed_data['setname'].astype(setname_order)

    # Sắp xếp DataFrame theo thứ tự setname
    processed_data.sort_values(by='setname', inplace=True)

    # Lưu kết quả vào file CSV mới
    processed_data.to_csv(output_file_path, index=False)
    print("done")

def Main():
    with open('./config/presolve/config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    file_path = config['file_path']
    output_file_path = config['output_file_path']
    setname_mapping = config['setname_mapping']
    order = config['order']
    convert_to_float = config['convert_to_float']
    
    # Gọi hàm để xử lý dữ liệu và lưu vào file mới
    process_data_by_setname(file_path, output_file_path, setname_mapping, order, convert_to_float)
