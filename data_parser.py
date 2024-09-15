import pandas as pd
import json
import requests

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

    def save_to_json(self, df_comment, df_effect, file_path):
        # 出力用のjsonデータを生成する
        output_data = {
            'comment': df_comment.to_dict(orient='records'),
            'effect': df_effect.to_dict(orient='records')
        }

        with open(file_path, 'w') as f:
            json.dump(output_data, f, indent=2)
