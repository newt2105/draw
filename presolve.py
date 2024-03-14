import pandas as pd

def process_data_by_setname(file_path, output_file_path):
    # Đọc dữ liệu từ file CSV
    df = pd.read_csv(file_path)

    # Tạo một bản sao của DataFrame để tránh ảnh hưởng đến dữ liệu gốc
    processed_data = df.copy()

    # Tạo một dictionary để ánh xạ giá trị setname với hệ số chia
    setname_mapping = {'DUMMY': 100, 'DUMMY2': 200, 'DUMMY04': 40, 'DUMMY07': 70}

    # Chuyển đổi kiểu dữ liệu của các cột sang float
    processed_data[['objvalue', 'usedlinksrate']] = processed_data[['objvalue', 'usedlinksrate']].astype(float)
    # print(processed_data)
    # processed_data['usednodescount'] /= processed_data['objvalue']
    # processed_data['usedlinkscount'] /= processed_data['objvalue']
    # print(processed_data)
    # Duyệt qua từng dòng và áp dụng hệ số chia tương ứng
    for setname, factor in setname_mapping.items():
        # print(setname, factor)
        mask = processed_data['setname'] == setname
        processed_data.loc[mask, ['objvalue']] /= factor

    # Xác định thứ tự ưu tiên của các giá trị setname
    setname_order = pd.CategoricalDtype(categories=['DUMMY04', 'DUMMY07', 'DUMMY', 'DUMMY2'], ordered=True)
    processed_data['setname'] = processed_data['setname'].astype(setname_order)

    # Sắp xếp DataFrame theo thứ tự setname
    processed_data.sort_values(by='setname', inplace=True)

    # Lưu kết quả vào file CSV mới
    processed_data.to_csv(output_file_path, index=False)

# Thay 'ten_file.csv' bằng đường dẫn đến file CSV thực tế của bạn
file_path = '20240308_101747.csv'
output_file_path = 'ten_file_processed3.csv'  # Đặt tên cho file CSV mới

# Gọi hàm để xử lý dữ liệu và lưu vào file mới
process_data_by_setname(file_path, output_file_path)
