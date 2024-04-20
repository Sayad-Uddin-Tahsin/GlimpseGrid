import psutil
import time
import threading
import os
from PIL import Image
import sys
import customtkinter as ctk
import json
import darkdetect


def resource_path(relative_path, data: bool = False, font: bool = False, network: bool = False, cpu: bool = False, base: bool = False) -> str:
    try:
        base_path = sys._MEIPASS2
    except Exception:
        dirlist = os.listdir(os.path.abspath("."))
        path = f"./"
        if "application" in dirlist:
            path += "application/"
            dirlist = os.listdir(path)
        if base:
            base_path = os.path.abspath(f"{path}assets")
            return os.path.join(base_path, relative_path)
        if "data" in dirlist and data:
            base_path = os.path.abspath(f"{path}data")
            return os.path.join(base_path, relative_path)

        if "assets" in dirlist:
            dirlist = os.listdir(os.path.abspath(f"{path}assets"))
            if "Font" in dirlist and font:
                base_path = os.path.abspath(f"{path}assets/Font")
            elif "Network" in dirlist and network:
                base_path = os.path.abspath(f"{path}assets/Network")
            elif "CPU" in dirlist and cpu:
                base_path = os.path.abspath(f"{path}assets/CPU")
            return os.path.join(base_path, relative_path)

ctk.FontManager.load_font(resource_path("TitilliumWeb.ttf", font=True))

class NetworkMonitorWidget:
    def __init__(self) -> None:
        self.upload_label = None
        self.download_label = None
        self.db = json.load(open(resource_path("config.json", data=True), "r"))

    def create_window(self) -> None:
        self.root = ctk.CTk()
        ctk.set_appearance_mode(self.db['NetworkMonitor']['theme'])
        self.transparent_color = "#000000"
        self.root.title("Network Widget")
        self.root.resizable(0, 0)
        self.root.configure(fg_color=self.transparent_color)
        self.root.wm_attributes('-transparentcolor', self.transparent_color)
        self.root.overrideredirect(1)
        self.root.geometry("0x0+1136+30")

    def format_speed(self, speed) -> str:
        speed_in_kbps = speed / 1024
        if speed_in_kbps < 0:
            return "0.00 Kbps"
        if speed_in_kbps < 1024:
            return f"{speed_in_kbps:.2f} Kbps"
        elif speed_in_kbps < 1024 * 1024:
            return f"{speed_in_kbps / 1024:.2f} Mbps"
        else:
            return f"{speed_in_kbps / (1024 * 1024):.2f} Gbps"

    def get_network_speed(self, interval) -> tuple[float, float]:
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

    def update_speed(self) -> None:
        for upload, download in self.get_network_speed(0.5):
            if self.upload_label:
                self.upload_label.configure(text=f" {self.format_speed(upload)}")
            if self.download_label:
                self.download_label.configure(text=f" {self.format_speed(download)}")
    
    def create_network_monitor(self) -> None:
        width = 0
        if self.db["NetworkMonitor"]['Upload']:
            upload_frame = ctk.CTkFrame(master=self.root, corner_radius=20, bg_color=self.transparent_color, width=200, height=60)
            upload_frame.place(x=0, y=0)

            self.upload_label = ctk.CTkLabel(master=upload_frame, text=" 0.00 Kbps", image=ctk.CTkImage(Image.open(resource_path("Upload.png", network=True)), Image.open(resource_path("Upload.png", network=True)), (40, 40)), compound="left", font=("Titillium Web", 20, "bold"))
            self.upload_label.place(x=8, y=8)
            width += 60
        
        if self.db["NetworkMonitor"]['Download']:
            if self.db["NetworkMonitor"]['Upload']:
                width += 10
            
            download_frame = ctk.CTkFrame(master=self.root, corner_radius=20, bg_color=self.transparent_color, width=200, height=60)
            download_frame.place(x=0, y=70 if self.db["NetworkMonitor"]['Upload'] else 0)

            self.download_label = ctk.CTkLabel(master=download_frame, text=" 0.00 Kbps", image=ctk.CTkImage(Image.open(resource_path("Download.png", network=True)), Image.open(resource_path("Download.png", network=True)), (40, 40)), compound="left", font=("Titillium Web", 20, "bold"))
            self.download_label.place(x=8, y=8)
            width += 60
        
        threading.Thread(target=self.update_speed, daemon=True).start()

        if self.db["NetworkMonitor"]['Upload'] or self.db["NetworkMonitor"]['Download']:
            self.root.geometry(f"200x{self.db['NetworkMonitor']['width']}+{self.db['NetworkMonitor']['x']}+{self.db['NetworkMonitor']['y']}")

            self.root.mainloop()
    
    def run(self) -> None:
        self.create_window()
        self.create_network_monitor()

if __name__ == "__main__":
    app = NetworkMonitorWidget()
    app.run()