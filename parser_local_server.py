from flask import *
import json
from time import sleep
from response_parser import ResponseParser

# prodで実行する場合
url = 'https://yaovxdll6j.execute-api.ap-northeast-1.amazonaws.com/school-fes-2024-UnityRequestReceiver'
# devで実行する場合
 # url = 'http://localhost:8888/'
response_interval = 5
output_file_path = 'data/output.json'

app = Flask(__name__)

@app.route("/")
def index():
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
    return json_data

if __name__ == "__main__":
    app.run(port=8080)