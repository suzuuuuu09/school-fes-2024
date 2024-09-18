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
        if not df_comment.empty and not df_effect.empty:
            min_df_comment = df_comment['timestamp'].min()
            min_df_effect = df_effect['timestamp'].min()

            min_timestamp = min(min_df_comment, min_df_effect)

            # timestampの差を計算
            df_comment['delay'] = (df_comment['timestamp'] - min_timestamp)
            df_effect['delay'] = (df_effect['timestamp'] - min_timestamp)

            df_comment['delay'].fillna(0).astype(int)
            df_effect['delay'].fillna(0).astype(int)

            # timestamp列を削除
            df_comment.drop(columns=['timestamp'], inplace=True)
            df_effect.drop(columns=['timestamp'], inplace=True)

            return df_comment, df_effect
        elif df_comment.empty and not df_effect.empty:
            min_df_effect = df_effect['timestamp'].min()
            df_effect['delay'] = (df_effect['timestamp'] - min_df_effect)
            df_effect['delay'].fillna(0).astype(int)
            df_effect.drop(columns=['timestamp'], inplace=True)
            return None, df_effect
        elif not df_comment.empty and df_effect.empty :
            min_df_comment = df_comment['timestamp'].min()
            df_comment['delay'] = (df_comment['timestamp'] - min_df_comment)
            df_comment['delay'].fillna(0).astype(int)
            df_comment.drop(columns=['timestamp'], inplace=True)
            return df_comment, None
        elif df_comment.empty and df_effect.empty:
            return None, None



    def json_data(self, df_comment, df_effect):
        # 出力用のjsonデータを生成
        output_data = {
            'comment': df_comment.to_dict(orient='records') if df_comment is not None else [],
            'effect': df_effect.to_dict(orient='records') if df_effect is not None else []
        }

        return json.dumps(output_data, indent=2)
