import psutil
import time
import threading
import os

def format_speed(speed):
    if speed < 1024:
        return f"{speed:.2f} bytes/s"
    elif speed < 1024 * 1024:
        return f"{speed / 1024:.2f} kbps"
    elif speed < 1024 * 1024 * 1024:
        return f"{speed / (1024 * 1024):.2f} Mbps"
    else:
        return f"{speed / (1024 * 1024 * 1024):.2f} Gbps"

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

# Print live upload and download speeds
for upload, download in get_network_speed():
    print(f"Upload Speed: {format_speed(upload)} | Download Speed: {format_speed(download)}")