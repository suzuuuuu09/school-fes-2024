from flask import Flask, request, render_template_string, jsonify

app = Flask(__name__)

data = []
HTML_TEMPLATE = '''
<!doctype html>
<html lang="ja">
  <head>
    <meta charset="utf-8">
    <title>Send comment</title>
  </head>
  <body>
    <h1>Send Comment</h1>
    <form method="post" action="/send">
      <label for="comment">Enter Comment:</label>
      <input type="text" id="comment" name="comment">
      <button type="submit">Send</button>
    </form>
    <h2>Received Comment:</h2>
    <pre>{{ received_comment }}</pre>
  </body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, received_comment='')

@app.route('/send', methods=['POST'])
def send_data():
    user_input = request.form['comment']
    data.append(user_input)
    # 受け取ったデータを表示
    return render_template_string(HTML_TEMPLATE, received_comment=user_input)

@app.route('/data', methods=['GET'])
def write_data():
    # リストを改行で結合して表示する
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
