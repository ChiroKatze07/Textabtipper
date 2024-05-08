import tkinter as tk
from tkinter import messagebox
import time
import threading
from pynput.keyboard import Controller, Key

class TypingApp:
    def __init__(self, master):
        self.master = master
        master.title("Textabtipper")
        master.geometry("500x500")

        self.header_label = tk.Label(master, text="Textabtipper", font=("Lucida Sans Unicode", 20))
        self.header_label.pack()

        self.label = tk.Label(master, text="Text eingeben:", font=("Lucida Sans Unicode", 10))
        self.label.pack()

        self.text_entry = tk.Text(master, height=10, width=50, font=("Arial", 9))
        self.text_entry.pack()

        self.delay_label = tk.Label(master, text="Verzögerung zwischen den Tasten (in Sekunden, mit . als Komma):", font=("Lucida Sans Unicode", 10))
        self.delay_label.pack()

        self.delay_entry = tk.Entry(master)
        self.delay_entry.pack()

        self.key_rate_label = tk.Label(master, text="", font=("Lucida Sans Unicode", 10))
        self.key_rate_label.pack()

        self.start_delay_label = tk.Label(master, text="Startverzögerung (in Sekunden, mit . als Komma):", font=("Lucida Sans Unicode", 10))
        self.start_delay_label.pack()

        self.start_delay_entry = tk.Entry(master)
        self.start_delay_entry.insert(0, "3")  # Standardstartverzögerung
        self.start_delay_entry.pack()

        self.loop_text = tk.BooleanVar()
        self.loop_checkbox = tk.Checkbutton(master, text="Endlos wiederholen", variable=self.loop_text)
        self.loop_checkbox.pack()

        self.start_button = tk.Button(master, text="Start", command=self.start_typing, font=("Lucida Sans Unicode", 10))
        self.start_button.pack()

        self.stop_button = tk.Button(master, text="Stopp", command=self.stop_typing, state=tk.DISABLED, font=("Lucida Sans Unicode", 10))
        self.stop_button.pack()

        self.info_button = tk.Button(master, text="Info", command=self.show_info, font=("Lucida Sans Unicode", 10))
        self.info_button.pack()

        self.thread = None
        self.stop_flag = False

    def start_typing(self):
        self.stop_flag = False
        text = self.text_entry.get("1.0", tk.END)
        delay = float(self.delay_entry.get())
        start_delay = float(self.start_delay_entry.get())

        if not text.strip():
            messagebox.showerror("Fehler", "Bitte geben Sie einen Text ein.", font=("Lucida Sans Unicode", 10))
            return

        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.info_button.config(state=tk.DISABLED)
        self.thread = threading.Thread(target=self.typing_thread, args=(text, delay, start_delay))
        self.thread.start()

    def stop_typing(self):
        self.stop_flag = True
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.info_button.config(state=tk.NORMAL)

    def typing_thread(self, text, delay, start_delay):
        time.sleep(start_delay)

        keyboard = Controller()
        while not self.stop_flag:
            for char in text:
                if self.stop_flag:
                    break
                keyboard.press(char)
                time.sleep(delay)
                keyboard.release(char)
            if not self.loop_text.get():
                break

        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.info_button.config(state=tk.NORMAL)

    def show_info(self):
        info_text = ("Textabtipper ist ein Programm, das einen eingefügten Text abschreibt. Im Gegensatz zu ähnlichen Programmen, unterstützt der Textabtipper auch Umlaute und ß. Das Programm wurde von ChiroKatze07 und mit Hilfe von Künstlicher Intelligenz entwickelt. Das Programm ist komplett gratis und wird auch immer so bleiben!\n\nBedinung: Text einfügen, Verzögerungen eingeben und auf Start drücken!")
        messagebox.showinfo("Info", info_text)

    def update_key_rate_label(self, event):
        try:
            delay_value = float(self.delay_entry.get())
            if delay_value > 0:
                keystrokes_per_10_minutes = int(600 / delay_value)
                self.key_rate_label.config(text=f"Anschläge in 10 Minuten: {keystrokes_per_10_minutes}")
        except ValueError:
            pass

def main():
    root = tk.Tk()
    app = TypingApp(root)
    app.delay_entry.bind("<KeyRelease>", app.update_key_rate_label)
    root.mainloop()

if __name__ == "__main__":
    main()
