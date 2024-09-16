import pandas as pd
import json
import requests
from time import sleep
from flask import *
import json

app = Flask(__name__)

class DataParser:
    def __init__(self, url):
        self.url = url

    def get_data(self):
        response = requests.get(self.url)
        return response.json()

    def parse_data(self, data):
        df_comment = pd.json_normalize(data['comment'])
        df_effect = pd.json_normalize(data['effect'])

        # timestampの一行上のtimestampとの差をdelay列に書き込む
        # 欠損値NaNを0とする
        # id_diff列のデータ型をintに変換する
        df_comment['delay'] = df_comment['timestamp'].diff().fillna(0).astype(int)
        df_effect['delay'] = df_effect['timestamp'].diff().fillna(0).astype(int)

        # timestamp列を削除する
        df_comment.drop(columns=['timestamp'], inplace=True)
        df_effect.drop(columns=['timestamp'], inplace=True)

        return df_comment, df_effect

    def json_data(self, df_comment, df_effect):
        # 出力用のjsonデータを生成する
        output_data = {
            'comment': df_comment.to_dict(orient='records'),
            'effect': df_effect.to_dict(orient='records')
        }

        return json.dumps(output_data, indent=2)

if __name__ == '__main__':
    url = 'https://yaovxdll6j.execute-api.ap-northeast-1.amazonaws.com/school-fes-2024-UnityRequestReceiver'
    response_interval = 5
    output_file_path = 'data/output.json'

    while True:
        parser = DataParser(url)
        data = parser.get_data()

        df_comment, df_effect = parser.parse_data(data)

        data = parser.json_data(df_comment, df_effect)
        with open(output_file_path, 'w') as f:
            f.write(data)
        print(data)
        sleep(response_interval)
