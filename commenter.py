import tkinter as tk
from time import sleep

MARGIN = 5000       # 余白
default_x = 1920    # 開始位置のx座標
default_y = 10      # 一行目のy座標
text_speed = 1     # 流れるスピード

def move():
    global default_x, text_speed
    label1.place_forget()  # ラベルを消去
    label1.place(x=default_x, y=default_y)  # ラベルを再配置
    default_x -= text_speed

    if default_x <= -label1.winfo_reqwidth():  # 画面左端まで文字が到達した場合
        root.destroy()     # 終了する

    root.after(1, move)  # 1ミリ秒ごとにスクロール


sleep(30)
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
label1 = tk.Label(root, textvariable=text_st, font=('', 45), background="white", foreground="gray99")
label1.place(x=default_x, y=default_y)

# スクロール処理を開始
move()

# イベントループを開始
root.mainloop()
