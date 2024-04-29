import psutil
import threading
import os
from PIL import Image
import sys
import customtkinter as ctk
import json
import logging
import sys

if not os.path.exists("./Logs"):
    os.makedirs("./Logs")
    
logging.basicConfig(filename='./Logs/CPU-Error.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def error_logger(exception_type, exception_value, exception_traceback):
    logging.error("Exception occurred:", exc_info=(exception_type, exception_value, exception_traceback))

sys.excepthook = error_logger

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

class CPUMonitorWidget:
    def __init__(self) -> None:
        self.name = "CPUMonitor"
        self.generate_shades()
        self.db = json.load(open(resource_path("config.json", data=True), "r"))
        self.image_dict = {
            0: "CPU 0 - 20.png",
            10: "CPU 0 - 20.png",
            20: "CPU 0 - 20.png",
            30: "CPU 30.png",
            40: "CPU 40.png",
            50: "CPU 50.png",
            60: "CPU 60.png",
            70: "CPU 70 - 100.png",
            80: "CPU 70 - 100.png",
            90: "CPU 70 - 100.png",
            100: "CPU 70 - 100.png"
        }
        self.last_percentage = 0

    def get_y_placement(self) -> int:
        temp_db = self.db.copy()
        y_placement = 30
        listed_db = list(temp_db.keys())
        for key in listed_db:
            if listed_db.index(key) >= listed_db.index(self.name):
                temp_db.pop(key)
        
        for widget in temp_db:
            if temp_db[widget]['status']:
                y_placement += temp_db[widget]["height"] + 10
        return y_placement

    def generate_shades(self) -> None:
        self.color_shades = {}
        start_color = (2, 206, 2)
        mid_color = (207, 204, 2)
        end_color = (207, 2, 2)

        r_step = (mid_color[0] - start_color[0]) / 50
        g_step_1 = (mid_color[1] - start_color[1]) / 50
        g_step_2 = (end_color[1] - mid_color[1]) / 50
        b_step = (mid_color[2] - start_color[2]) / 50

        for i in range(101):
            r = int(start_color[0] + i * r_step)
            if i <= 25:
                g = int(start_color[1] + i * g_step_1)
            else:
                g = int(mid_color[1] + (i - 25) * g_step_2)
            b = int(start_color[2] + i * b_step)
            self.color_shades[i] = (r, g, b)
    
    def image_to_be_changed(self, percentage):
        groups = [[0, 10, 20], [30], [40], [50], [60], [70, 80, 90, 100]]

        last_percentage_index = 0
        current_percentage_index = 0
        for group in groups:
            if self.last_percentage in group:
                last_percentage_index = groups.index(group)
            elif (int(percentage) // 10) * 10 in group:
                current_percentage_index = groups.index(group)
        
        self.last_percentage = (int(percentage) // 10) * 10
        
        if last_percentage_index == current_percentage_index:
            return False
        else:
            return True

    def get_color(self, percentage: int) -> str:
        rgb = self.color_shades.get(percentage)
        r = max(0, min(255, rgb[0]))
        g = max(0, min(255, rgb[1]))
        b = max(0, min(255, rgb[2]))
        return '#{:02x}{:02x}{:02x}'.format(r, g, b)
    
    def get_cpu_usage(self) -> float:
        while True:
            yield psutil.cpu_percent(interval=1)
    
    def update_usage(self, labelobj: ctk.CTkLabel) -> None:
        for usage in self.get_cpu_usage():
            # labelobj.configure(text_color=self.get_color(int(usage)), text=f" {usage:.2f}%")
            if self.db[f'{self.name}']['dynamic_icon']:
                if self.image_to_be_changed(int(usage)):
                    labelobj.configure(text_color=self.get_color(int(usage)), text=f" {usage:.2f}%", image=ctk.CTkImage(Image.open(resource_path(self.get_image(int(usage)), cpu=True)), Image.open(resource_path(self.get_image(int(usage)), cpu=True)), (40, 40)))
                else:
                    labelobj.configure(text_color=self.get_color(int(usage)), text=f" {usage:.2f}%")
            else:
                labelobj.configure(text_color=self.get_color(int(usage)), text=f" {usage:.2f}%")

    def get_image(self, percentage: int):
        return resource_path(self.image_dict.get((int(percentage) // 10) * 10), cpu=True)

    def create_window(self) -> None:
        self.root = ctk.CTk()
        self.root.config(bg='#000000')
        ctk.set_appearance_mode(self.db[f'{self.name}']['theme'])
        self.root.title("CPU Widget")
        self.root.resizable(0, 0)
        self.root.wm_attributes('-transparentcolor','#000000')
        self.root.overrideredirect(1)
        self.root.geometry("0x0+1136+30")
    
    def create_cpu_monitor(self):
        usage_frame = ctk.CTkFrame(self.root, corner_radius=20, bg_color="#000000", width=135, height=60)
        usage_frame.place(x=0, y=0)

        if self.db[f'{self.name}']['dynamic_icon']:
            usage_label = ctk.CTkLabel(master=usage_frame, text=" 0.00%", text_color=self.get_color(0), image=ctk.CTkImage(Image.open(resource_path("CPU 0 - 20.png", cpu=True)), Image.open(resource_path("CPU 0 - 20.png", cpu=True)), (40, 40)), compound="left", font=("Titillium Web", 20, "bold"))
        else:
            usage_label = ctk.CTkLabel(master=usage_frame, text=" 0.00%", text_color=self.get_color(0), image=ctk.CTkImage(Image.open(resource_path("CPU Light.png", cpu=True)), Image.open(resource_path("CPU Dark.png", cpu=True)), (40, 40)), compound="left", font=("Titillium Web", 20, "bold"))
        usage_label.place(x=8, y=8)

        threading.Thread(target=self.update_usage, args=(usage_label, ), daemon=True).start()
        self.root.geometry(f"135x{self.db[f'{self.name}']['height']}")
        self.root.geometry(f"+{(self.root.winfo_screenwidth() - 135) - 30}+{self.get_y_placement()}")
        self.root.mainloop()

    def run(self) -> None:
        self.create_window()
        self.create_cpu_monitor()
        
if __name__ == "__main__":
    app = CPUMonitorWidget()
    app.run()