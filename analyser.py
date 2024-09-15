import pandas as pd
import json

file_path = 'test.json'
output_file_path = 'output.json'

# JSONファイルの内容を手動で確認
with open(file_path, 'r') as f:
    try:
        data = json.load(f)
    except json.JSONDecodeError as e:
        exit()

# `comment`と`effect`のデータを確認
if 'comment' not in data or 'effect' not in data:
    print("The JSON file does not contain 'comment' and 'effect' keys.")
    exit()

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

# 出力用のjsonデータを生成する
output_data = {
    'comment': df_comment.to_dict(orient='records'),
    'effect': df_effect.to_dict(orient='records')
}

with open(output_file_path, 'w') as f:
    json.dump(output_data, f, indent=2)

