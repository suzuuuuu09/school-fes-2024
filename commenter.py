import tkinter as tk
from time import sleep

MARGIN = 5000       # 余白
DEFAULT_X = 1920    # 開始位置のx座標
DEFAULT_Y = 10      # 一行目のy座標
TEXT_SPEED_BASE = 1     # 流れるスピード

def move():
    global DEFAULT_X, TEXT_SPEED_BASE
    for i, target in labelDist.items():
        target.place_forget()  # ラベルを消去
        target.place(x=DEFAULT_X, y=DEFAULT_Y + 50*i)  # ラベルを再配置
        DEFAULT_X -= TEXT_SPEED_BASE

        if DEFAULT_X <= -target.winfo_reqwidth():  # 画面左端まで文字が到達した場合
            root.destroy()     # 終了する
    
    print(labelDist)
    root.after(1, move)  # 1ミリ秒ごとにスクロール


# ウィンドウの初期化
root = tk.Tk()
sWidth = root.winfo_width()
sHeight = root.winfo_height()
root.attributes("-transparentcolor", "white")  # 背景を透明にする色を設定
root.attributes("-fullscreen", True)  # フルスクリーンに設定
root.attributes("-topmost", True)   # ウィンドウを最前面に設定

# キャンバスを作成してウィンドウに配置
canvas = tk.Canvas(root, width=sWidth+MARGIN, height=sHeight+MARGIN, background="white")
canvas.place(x=-(MARGIN/2), y=-(MARGIN/2))


text = "あめんぼあかいなあいうえお"
text_st = tk.StringVar()
text_st.set(text)

# ラベルを作成し、キャンバスに配置
labelDist = {}
for i in range(5):
    labelDist[i] = tk.Label(root, textvariable=text_st, font=('', 45), background="white", foreground="gray99")
    labelDist[i].place(x=DEFAULT_X - 700, y=DEFAULT_Y + 75*i)

move()

# スクロール処理を開始

# イベントループを開始
root.mainloop()
