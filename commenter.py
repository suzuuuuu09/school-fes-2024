import tkinter as tk

# ウィンドウの初期化
root = tk.Tk()
root.geometry("1920x1080")  # ウィンドウサイズを設定
root.attributes("-transparentcolor", "white")  # 背景を透明にする色を設定
root.attributes("-fullscreen", True)  # フルスクリーンに設定

# キャンバスを作成してウィンドウに配置
canvas = tk.Canvas(root, width=1920, height=1080, background="white", highlightthickness=0)
canvas.place(x=0, y=0)

# 初期位置とリストの設定
default_x = 1920
default_y = 5
text_speed = 50     # テキストの動く速さ
text = "あめんぼあかいなあいうえお"
text_st = tk.StringVar()
text_st.set(text)

# ラベルを作成し、キャンバスに配置
label1 = tk.Label(root, textvariable=text_st, font=('', 45), background="white", foreground="gray99")
label1.place(x=default_x, y=default_y)

def move():
    global default_x, text_speed
    label1.place_forget()  # ラベルを消去
    label1.place(x=default_x, y=default_y)  # ラベルを再配置
    default_x -= text_speed

    if default_x <= -canvas.winfo_width():  # 画面左端まで文字が到達した場合
        root.destroy()     # 終了する

    root.after(100, move)  # 100ミリ秒ごとにスクロール

# スクロール処理を開始
move()

# イベントループを開始
root.mainloop()
