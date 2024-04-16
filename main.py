import psutil
import time
import threading
import os
from PIL import Image
import sys
import customtkinter as ctk
import json

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        dirlist = os.listdir(os.path.abspath("."))
        if "Assets" in dirlist:
            base_path = os.path.abspath("./Assets")
    return os.path.join(base_path, relative_path)

ctk.FontManager.load_font(resource_path("TitilliumWeb.ttf"))

class NetworkMonitorWidget:
    def __init__(self):
        with open("data.json", 'r') as f:
            self.db = json.load(f)
            
        self.root = ctk.CTk()
        self.root.config(bg='#000000')
        ctk.set_appearance_mode("dark")
        self.root.wm_attributes('-transparentcolor','#000000')
        self.root.overrideredirect(1)
        self.root.geometry("0x0+1136+30")
        
        self.upload_label = None
        self.download_label = None

    def format_speed(self, speed):
        speed_in_kbps = speed / 1024
        if speed_in_kbps < 0:
            return "0.00 Kbps"
        if speed_in_kbps < 1024:
            return f"{speed_in_kbps:.2f} Kbps"
        elif speed_in_kbps < 1024 * 1024:
            return f"{speed_in_kbps / 1024:.2f} Mbps"
        else:
            return f"{speed_in_kbps / (1024 * 1024):.2f} Gbps"

    def get_network_speed(self, interval):
        last_bytes_sent = psutil.net_io_counters().bytes_sent
        last_bytes_recv = psutil.net_io_counters().bytes_recv
        
        while True:
            bytes_sent = psutil.net_io_counters().bytes_sent
            bytes_recv = psutil.net_io_counters().bytes_recv
            
            upload_speed = (bytes_sent - last_bytes_sent) / interval
            download_speed = (bytes_recv - last_bytes_recv) / interval
            
            last_bytes_sent = bytes_sent
            last_bytes_recv = bytes_recv
            
            yield upload_speed, download_speed
            
            time.sleep(interval)

    def update_speed(self):
        for upload, download in self.get_network_speed(0.5):
            if self.upload_label:
                self.upload_label.configure(text=f" {self.format_speed(upload)}")
            if self.download_label:
                self.download_label.configure(text=f" {self.format_speed(download)}")

    def network_monitor(self):
        width = 0
        if self.db["NetworkMonitor"]['Upload']:
            upload_frame = ctk.CTkFrame(self.root, corner_radius=20, bg_color="#000000", width=200, height=60)
            upload_frame.place(x=0, y=0)

            self.upload_label = ctk.CTkLabel(upload_frame, text=" 0.00 Kbps", image=ctk.CTkImage(Image.open(resource_path("Upload.png")), Image.open(resource_path("Upload.png")), (40, 40)), compound="left", font=("Titillium Web", 20, "bold"))
            self.upload_label.place(x=8, y=8)
            width += 60
        
        if self.db["NetworkMonitor"]['Download']:
            if self.db["NetworkMonitor"]['Upload']:
                width += 10
            
            download_frame = ctk.CTkFrame(self.root, corner_radius=20, bg_color="#000000", width=200, height=60)
            download_frame.place(x=0, y=70 if self.db["NetworkMonitor"]['Upload'] else 0)

            self.download_label = ctk.CTkLabel(download_frame, text=" 0.00 Kbps", image=ctk.CTkImage(Image.open(resource_path("Download.png")), Image.open(resource_path("Download.png")), (40, 40)), compound="left", font=("Titillium Web", 20, "bold"))
            self.download_label.place(x=8, y=8)
            width += 60
        
        threading.Thread(target=self.update_speed, daemon=True).start()

        if self.db["NetworkMonitor"]['Upload'] or self.db["NetworkMonitor"]['Download']:
            self.root.geometry(f"200x{width}+1136+30")
            self.root.mainloop()

if __name__ == "__main__":
    app = NetworkMonitorWidget()
    app.network_monitor()
