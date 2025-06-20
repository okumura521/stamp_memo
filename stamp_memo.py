# グラフ描画ライブラリ（matplotlib）をインポート
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm  # 日本語フォント指定に使う
from collections import Counter       # スタンプ別の件数を集計
import json, os                       # ファイル読み書きと存在チェック
import tkinter as tk                 # 標準GUIライブラリ
from tkinter import messagebox, Listbox, END, Scrollbar  # GUI部品
from datetime import datetime         # 日付・時刻の取得

# Windowsにあるメイリオフォントのパスを指定（絵文字や日本語対応）
font_path = "C:/Windows/Fonts/meiryo.ttc"
font_prop = fm.FontProperties(fname=font_path)

DATA_FILE = "memos.json"  # メモデータを保存するJSONファイル名

# --- メモをファイルから読み込む関数（存在しない場合は空リスト） ---
def load_memos():
    if os.path.exists(DATA_FILE):
        return json.load(open(DATA_FILE, encoding="utf-8"))
    return []

# --- メモをファイルに保存する関数 ---
def save_memos(memos):
    json.dump(memos, open(DATA_FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

# --- アプリのメイン処理 ---
def main():
    memos = load_memos()  # 既存のメモを読み込み
    stamps = ["★", "完了", "注意"]  # スタンプの選択肢
    current_stamp = [stamps[0]]  # 現在選択中のスタンプ（リストでmutable）

    # --- スタンプが押されたときに現在のスタンプを更新 ---
    def on_stamp_click(stamp):
        current_stamp[0] = stamp

    # --- 「追加」ボタン押下時の処理 ---
    def on_add():
        txt = text_input.get("1.0", END).strip()  # 入力欄からテキスト取得
        if not txt:
            return
        entry = {
            "text": txt,
            "stamp": current_stamp[0],
            "time": datetime.now().isoformat()
        }
        memos.append(entry)         # メモを追加
        save_memos(memos)          # ファイルに保存
        update_list()              # 表示を更新
        text_input.delete("1.0", END)  # 入力欄をクリア

    # --- 「削除」ボタン押下時の処理（選択されたメモを削除） ---
    def on_delete():
        selected = log_list.curselection()  # 選択インデックス取得
        if not selected:
            messagebox.showinfo("削除", "削除するメモを選択してください")
            return
        index = selected[0]
        del memos[index]             # リストから削除
        save_memos(memos)           # ファイル更新
        update_list()               # 表示を更新

    # --- 「終了」ボタン押下時の処理 ---
    def on_exit():
        root.destroy()  # アプリを終了

    # --- メモ一覧をListboxに反映する関数 ---
    def update_list():
        log_list.delete(0, END)  # 一度クリア
        for m in memos:
            log_list.insert(END, f"{m['stamp']} {m['text']}")

    # --- 「グラフ表示」ボタン押下時の処理 ---
    def show_stamp_chart():
        stamp_counts = Counter(m['stamp'] for m in memos)  # スタンプごとにカウント
        if not stamp_counts:
            messagebox.showinfo("情報", "まだメモが登録されていません")
            return
        stamps = list(stamp_counts.keys())
        counts = list(stamp_counts.values())

        # グラフ作成
        plt.figure(figsize=(6,4))
        plt.bar(stamps, counts, color="skyblue")
        plt.title("スタンプ別 メモ数", fontproperties=font_prop)
        plt.xlabel("スタンプ", fontproperties=font_prop)
        plt.ylabel("件数", fontproperties=font_prop)
        plt.xticks(fontproperties=font_prop)
        plt.tight_layout()
        plt.show()

    # --- GUI構築ここから ---
    root = tk.Tk()  # メインウィンドウ作成
    root.title("スタンプメモ")
    root.geometry("400x400")  # ウィンドウサイズ設定

    text_input = tk.Text(root, height=3, width=40)  # メモ入力欄
    text_input.pack(pady=5)

    # --- スタンプボタンエリアの作成 ---
    stamp_frame = tk.Frame(root)
    tk.Label(stamp_frame, text="スタンプ:").pack(side=tk.LEFT)
    for s in stamps:
        tk.Button(stamp_frame, text=s, width=4, command=lambda s=s: on_stamp_click(s)).pack(side=tk.LEFT)
    stamp_frame.pack(pady=5)

    # --- 操作ボタン（追加／削除／終了／グラフ表示） ---
    action_frame = tk.Frame(root)
    tk.Button(action_frame, text="追加", width=10, command=on_add).pack(side=tk.LEFT, padx=5)
    tk.Button(action_frame, text="削除", width=10, command=on_delete).pack(side=tk.LEFT, padx=5)
    tk.Button(action_frame, text="終了", width=10, command=on_exit).pack(side=tk.LEFT, padx=5)
    tk.Button(action_frame, text="グラフ表示", width=10, command=show_stamp_chart).pack(side=tk.LEFT, padx=5)
    action_frame.pack(pady=5)

    # --- ログ表示（メモのリスト） ---
    tk.Label(root, text="ログ").pack()
    list_frame = tk.Frame(root)
    log_list = Listbox(list_frame, width=50, height=10)  # メモ一覧
    scrollbar = Scrollbar(list_frame, orient=tk.VERTICAL, command=log_list.yview)  # 縦スクロールバー
    log_list.config(yscrollcommand=scrollbar.set)
    log_list.pack(side=tk.LEFT, fill=tk.BOTH)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    list_frame.pack()

    update_list()       # 初期表示反映
    root.mainloop()     # GUIイベントループ開始

# --- スクリプトが直接実行されたときだけmain()を呼び出す ---
if __name__ == "__main__":
    main()