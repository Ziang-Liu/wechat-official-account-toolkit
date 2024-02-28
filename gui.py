import tkinter as tk
from tkinter.ttk import *
import threading, ctypes, sys
from article_fetcher import get_page_list

def start():
    cookie = entry1.get()
    user_agent = entry2.get()
    fakeid = entry3.get()
    token = entry4.get()
    
    task_thread = threading.Thread(target=get_page_list, args=(cookie,user_agent,fakeid,token))
    task_thread.start()

def button_pressed():
    start()

window = tk.Tk()
window.title("WeChat Official Account Fetcher")
window.resizable(False, False)

ctypes.windll.shcore.SetProcessDpiAwareness(1)
ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
window.tk.call('tk', 'scaling', ScaleFactor/75)

input_frame = tk.Frame(window, padx=10, pady=10)
input_frame.pack(fill="both", expand=True)

label1 = tk.Label(input_frame, text="Cookies")
label1.grid(row=0, column=0, sticky="w")
entry1 = tk.Entry(input_frame, width=40)
entry1.grid(row=0, column=1, padx=10, sticky="we")

label2 = tk.Label(input_frame, text="User Agent")
label2.grid(row=1, column=0, sticky="w")
entry2 = tk.Entry(input_frame, width=40)
entry2.grid(row=1, column=1, padx=10, sticky="we")

label3 = tk.Label(input_frame, text="Fakeid")
label3.grid(row=2, column=0, sticky="w")
entry3 = tk.Entry(input_frame, width=40)
entry3.grid(row=2, column=1, padx=10, sticky="we")

label4 = tk.Label(input_frame, text="Token")
label4.grid(row=3, column=0, sticky="w")
entry4 = tk.Entry(input_frame, width=40)
entry4.grid(row=3, column=1, padx=10, sticky="we")

button = tk.Button(input_frame, text="Start fetching pages", command=start)
button.grid(row=4, columnspan=3, pady=10)

window.geometry("700x250")

window.mainloop()
