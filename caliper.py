import tkinter as tk
from tkinter import font as tkfont
import serial
import threading

# Configurare port Serial
PORT = 'COM3'
BAUD = 9600

class CaliperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Citire Șubler Digital - COM3")
        self.root.geometry("450x250")  # Aici este formatul corect (șir cu 'x', nu două argumente)
        self.root.configure(bg="#1e1e1e")
        self.root.resizable(False, False)

        # Stare conexiune / valori
        self.serial_conn = None
        self.is_running = True

        # Stiluri / Fonturi
        self.title_font = tkfont.Font(family="Helvetica", size=12, weight="bold")
        self.value_font = tkfont.Font(family="Consolas", size=36, weight="bold")
        self.unit_font = tkfont.Font(family="Helvetica", size=16, weight="bold")

        # Interfață grafică
        self.create_widgets()

        # Pornire fir de execuție pentru serial
        self.thread = threading.Thread(target=self.read_serial, daemon=True)
        self.thread.start()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_widgets(self):
        # Titlu
        lbl_title = tk.Label(self.root, text="VALOARE ȘUBLER", font=self.title_font, fg="#888888", bg="#1e1e1e")
        lbl_title.pack(pady=(20, 5))

        # Cadru pentru valoare și unitate
        frame_val = tk.Frame(self.root, bg="#1e1e1e")
        frame_val.pack(pady=10)

        self.lbl_value = tk.Label(frame_val, text="---.--", font=self.value_font, fg="#00ffcc", bg="#1e1e1e")
        self.lbl_value.pack(side=tk.LEFT)

        self.lbl_unit = tk.Label(frame_val, text="mm", font=self.unit_font, fg="#ffaa00", bg="#1e1e1e")
        self.lbl_unit.pack(side=tk.LEFT, padx=(10, 0), pady=(15, 0))

        # Status conexiune
        self.lbl_status = tk.Label(self.root, text=f"Se conectează la {PORT}...", font=("Helvetica", 10), fg="#ff5555", bg="#1e1e1e")
        self.lbl_status.pack(side=tk.BOTTOM, pady=15)

    def read_serial(self):
        try:
            self.serial_conn = serial.Serial(PORT, BAUD, timeout=1)
            self.root.after(0, lambda: self.lbl_status.config(text=f"Conectat la {PORT}", fg="#55ff55"))
        except Exception as e:
            self.root.after(0, lambda: self.lbl_status.config(text=f"Eroare conectare: {e}", fg="#ff5555"))
            return

        while self.is_running:
            try:
                if self.serial_conn and self.serial_conn.in_waiting:
                    line = self.serial_conn.readline().decode('utf-8', errors='ignore').strip()
                    if line:
                        parts = line.split()
                        if len(parts) >= 2:
                            val_str, unit_str = parts[0], parts[1]
                            self.root.after(0, lambda v=val_str, u=unit_str: self.update_display(v, u))
            except Exception:
                break

    def update_display(self, val, unit):
        self.lbl_value.config(text=val)
        self.lbl_unit.config(text=unit)

    def on_close(self):
        self.is_running = False
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CaliperApp(root)
    root.mainloop()