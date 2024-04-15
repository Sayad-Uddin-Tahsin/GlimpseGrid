import psutil
import time
import threading
import os
from PIL import Image
import sys
import customtkinter as ctk


def format_speed(speed):
    speed_in_kbps = speed / 1024
    if speed_in_kbps < 1024:
        return f"{speed_in_kbps:.2f} Kbps"
    elif speed_in_kbps < 1024 * 1024:
        return f"{speed_in_kbps / 1024:.2f} Mbps"
    else:
        return f"{speed_in_kbps / (1024 * 1024):.2f} Gbps"


def get_network_speed(interval=1):
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


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        dirlist = os.listdir(os.path.abspath("."))
        if "Assets" in dirlist:
            base_path = os.path.abspath("./Assets")
    return os.path.join(base_path, relative_path)

ctk.FontManager.load_font(resource_path("TitilliumWeb.ttf"))

def update_speed(uploadLabel: ctk.CTkLabel=None, downloadLabel: ctk.CTkLabel=None):
    if uploadLabel or downloadLabel:
        for upload, download in get_network_speed():
            if uploadLabel:
                uploadLabel.configure(text=f" {format_speed(upload)}")
            if downloadLabel:
                downloadLabel.configure(text=f" {format_speed(download)}")


def uploadWindow():
    root = ctk.CTk()
    root.geometry("200x130+1136+30")
    root.config(bg='#000000')
    ctk.set_appearance_mode("dark")
    root.wm_attributes('-transparentcolor','#000000')
    root.overrideredirect(True)

    uploadFrame = ctk.CTkFrame(root, corner_radius=20, bg_color="#000000", width=200, height=60)
    uploadFrame.place(x=0, y=0)

    uvalueLabel = ctk.CTkLabel(uploadFrame, text=" 0.00 Kbps", image=ctk.CTkImage(Image.open(resource_path("Upload.png")), Image.open(resource_path("Upload.png")), (40, 40)), compound="left", font=("Titillium Web", 20, "bold"))
    uvalueLabel.place(x=8, y=8)

    downloadFrame = ctk.CTkFrame(root, corner_radius=20, bg_color="#000000", width=200, height=60)
    downloadFrame.place(x=0, y=70)

    dvalueLabel = ctk.CTkLabel(downloadFrame, text=" 0.00 Kbps", image=ctk.CTkImage(Image.open(resource_path("Download.png")), Image.open(resource_path("Download.png")), (40, 40)), compound="left", font=("Titillium Web", 20, "bold"))
    dvalueLabel.place(x=8, y=8)

    threading.Thread(target=update_speed, args=(uvalueLabel, dvalueLabel, ), daemon=True).start()

    root.mainloop()

uploadWindow()