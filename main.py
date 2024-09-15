import pandas as pd
from data_parser import DataParser
from time import sleep

# URLからデータを取得
url = 'http://localhost:8888'
response_interval = 5
output_file_path = 'output.json'

while True:
    # JSONデータの取得と解析
    parser = DataParser(url)
    data = parser.get_data()

    # JSONデータを解析
    df_comment, df_effect = parser.parse_data(data)

    # JSONファイルに保存
    parser.save_to_json(df_comment, df_effect, output_file_path)
    sleep(response_interval)
