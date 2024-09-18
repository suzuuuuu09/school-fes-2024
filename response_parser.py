import pandas as pd
import json
import requests
from time import sleep
from flask import Flask

app = Flask(__name__)

class ResponseParser:
    def __init__(self, url):
        self.url = url

    def get_data(self):
        response = requests.get(self.url)
        return response.json()

    def parse_data(self, data):
        df_comment = pd.json_normalize(data['comment'])
        df_effect = pd.json_normalize(data['effect'])

        if df_comment is not None and not df_comment.empty:
           min_df_comment = df_comment['timestamp'].min()
        else:
            min_df_comment = None

        if df_effect is not None and not df_effect.empty:
            min_df_effect = df_effect['timestamp'].min()
        else:
            min_df_effect = None

        if min_df_comment is not None and min_df_effect is not None:
            min_timestamp = min(min_df_comment, min_df_effect)

            # timestampの差を計算
            df_comment['delay'] = (df_comment['timestamp'] - min_timestamp).fillna(0).astype(int)
            df_effect['delay'] = (df_effect['timestamp'] - min_timestamp).fillna(0).astype(int)

            # timestamp列を削除
            df_comment.drop(columns=['timestamp'], inplace=True)
            df_effect.drop(columns=['timestamp'], inplace=True)

            return df_comment, df_effect
        elif min_df_comment is None and min_df_effect is not None:
            return None, df_effect
        elif min_df_effect is None and min_df_comment is not None:
            return df_comment, None
        else:
            return None, None

    def json_data(self, df_comment, df_effect):
        # 出力用のjsonデータを生成
        output_data = {
            'comment': df_comment.to_dict(orient='records') if df_comment is not None else [],
            'effect': df_effect.to_dict(orient='records') if df_effect is not None else []
        }

        return json.dumps(output_data, indent=2)

if __name__ == '__main__':
    # prodで実行する場合
    # url = 'https://yaovxdll6j.execute-api.ap-northeast-1.amazonaws.com/school-fes-2024-UnityRequestReceiver'
    # devで実行する場合
    url = 'http://localhost:8888/'
    response_interval = 5
    output_file_path = 'data/output.json'

    while True:
        parser = ResponseParser(url)
        data = parser.get_data()
        try:
            df_comment, df_effect = parser.parse_data(data)
        except Exception as e:
            print(f"Error parsing data: {e}")
            df_comment, df_effect = None, None    

        json_data = parser.json_data(df_comment, df_effect)
        with open(output_file_path, 'w') as f:
            f.write(json_data)
        print(json_data)
        sleep(response_interval)
