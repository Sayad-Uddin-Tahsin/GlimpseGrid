import threading
import os
from PIL import Image
import sys
import customtkinter as ctk
import pystray
import subprocess
import os
import time
import json
import darkdetect
import psutil
import multiprocessing

def resource_path(relative_path, data: bool = False, font: bool = False, network: bool = False, cpu: bool = False, base: bool = False, example: bool = False) -> str:
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
        if example:
            base_path = os.path.abspath(f"{path}assets/Examples")
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

widgets = [
    ["CPUMonitor", "CPU Widget", "application/cpu.py", "CPU Widget.exe"],
    ["NetworkMonitor", "Network Widget", "application/network.py", "Network Widget.exe"]
]

ctk.FontManager.load_font(resource_path("NotoSans-Regular", font=True))
ctk.FontManager.load_font(resource_path("TitilliumWeb.ttf", font=True))

class MainEXE:
    def __init__(self) -> None:
        self.running_processes = {}
        self.db = json.load(open(resource_path("config.json", data=True), "r"))
        self.icon = None

    def _run_process(self, process_name: str, script_path: str):
        script_process = subprocess.Popen([script_path])
        self.running_processes[process_name] = script_process

    def _run_script(self, process_name: str, script_path: str):
        threading.Thread(target=self._run_process, args=(process_name, script_path, ), daemon=True).start()

    def _stop_script(self, icon: pystray.Icon, item: pystray.MenuItem):
        self.running_processes[str(item.__name__)].terminate()
        self.running_processes.pop(str(item.__name__))
        if len(self.running_processes) == 0:
            icon.stop()
            os._exit(0)
        else:
            icon.menu = pystray.Menu(
                pystray.MenuItem('Settings', self.open_settings, default=True),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem("Close",  self.generate_submenu(False)),
                pystray.MenuItem('Close All', self.exit_action)
            )
            icon.update_menu()
    
    def exit_action(self, icon, item) -> None:
        for process_name in self.running_processes:
            self.running_processes[process_name].terminate()
        icon.stop()
        os._exit(0)

    def open_settings(self, icon, item):
        settings = SettingsWindow()
        settings.run()
    
    def generate_submenu(self, start: bool=True):
        if start:
            time.sleep(1)
        items = []
        for process_name in self.running_processes:
            items.append(
                pystray.MenuItem(process_name, self._stop_script)
            )
        return pystray.Menu(*items)
    
    def run_on_systray(self) -> None:
        image = Image.open(resource_path(relative_path='Icon.png', base=True))

        icon = pystray.Icon(
            "name", 
            image,
            "Widget",
            menu=pystray.Menu(
                pystray.MenuItem('Settings', self.open_settings, default=True),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem("Close",  self.generate_submenu()),
                pystray.MenuItem('Close All', self.exit_action)
                )
        )
        self.icon = icon
        icon.run()

    def rerun(self):
        self.icon.stop()
        for process_name in self.running_processes:
            self.running_processes[process_name].terminate()
        self.db = json.load(open(resource_path("config.json", data=True), "r"))
        self.run()
    
    def run(self):
        for databasekey, process_name, _, script_path in widgets:
            if self.db[databasekey]['status']:
                threading.Thread(target=self._run_script, args=(process_name, script_path, ), daemon=True).start()
        self.run_on_systray()
    

class MainPY:
    def __init__(self) -> None:
        self.running_processes = {}
        self.db = json.load(open(resource_path("config.json", data=True), "r"))
        self.icon = None

    def _run_process(self, process_name: str, script_path: str):
        script_process = subprocess.Popen(['python', script_path])
        self.running_processes[process_name] = script_process

    def _run_script(self, process_name: str, script_path: str):
        threading.Thread(target=self._run_process, args=(process_name, script_path, ), daemon=True).start()

    def _stop_script(self, icon: pystray.Icon, item: pystray.MenuItem):
        self.running_processes[str(item.__name__)].terminate()
        self.running_processes.pop(str(item.__name__))
        if len(self.running_processes) == 0:
            icon.stop()
            os._exit(0)
        else:
            icon.menu = pystray.Menu(
                pystray.MenuItem('Settings', self.open_settings, default=True),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem("Close",  self.generate_submenu(False)),
                pystray.MenuItem('Close All', self.exit_action)
            )
            icon.update_menu()
    
    def exit_action(self, icon, item) -> None:
        for process_name in self.running_processes:
            self.running_processes[process_name].terminate()
        icon.stop()
        os._exit(0)

    def open_settings(self, icon, item):
        self.settings = SettingsWindow()
        self.settings.run()
    
    def generate_submenu(self, start: bool=True):
        if start:
            time.sleep(1)
        items = []
        for process_name in self.running_processes:
            items.append(
                pystray.MenuItem(process_name, self._stop_script)
            )
        return pystray.Menu(*items)
    
    def run_on_systray(self) -> None:
        image = Image.open(resource_path(relative_path='Icon.png', base=True))

        icon = pystray.Icon(
            "name", 
            image,
            "Widget",
            menu=pystray.Menu(
                pystray.MenuItem('Settings', self.open_settings, default=True),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem("Close",  self.generate_submenu()),
                pystray.MenuItem('Close All', self.exit_action)
                )
        )
        self.icon = icon
        icon.run()
    
    def rerun(self):
        self.icon.stop()
        for process_name in self.running_processes:
            self.running_processes[process_name].terminate()
        self.db = json.load(open(resource_path("config.json", data=True), "r"))
        self.run()

    def run(self):
        for databasekey, process_name, script_path, _ in widgets:
            if self.db[databasekey]['status']:
                threading.Thread(target=self._run_script, args=(process_name, script_path, ), daemon=True).start()
        self.run_on_systray()

class CPUMonitorWidget:
    def __init__(self, root: ctk.CTkFrame, db: dict) -> None:
        super().__init__()
        self.generate_shades()
        self.db = db
        self.theme = self.db["CPUMonitor"]['theme']
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
        self.root = root
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()
 
    def stopped(self):
        return self._stop.is_set()
    
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
    
    def destroy_all(self):
        for child in self.root.winfo_children():
            child.destroy()
        
    def update_usage(self, labelobj: ctk.CTkLabel) -> None:
        for usage in self.get_cpu_usage():
            if self.stopped():
                break
            if self.db['CPUMonitor']['dynamic_icon']:
                if self.image_to_be_changed(int(usage)):
                    labelobj.configure(text_color=self.get_color(int(usage)), text=f" {usage:.2f}%", image=ctk.CTkImage(Image.open(resource_path(self.get_image(int(usage)), cpu=True)), Image.open(resource_path(self.get_image(int(usage)), cpu=True)), (40, 40)))
                else:
                    labelobj.configure(text_color=self.get_color(int(usage)), text=f" {usage:.2f}%")
            else:
                labelobj.configure(text_color=self.get_color(int(usage)), text=f" {usage:.2f}%")

    def get_image(self, percentage: int):
        return resource_path(self.image_dict.get((int(percentage) // 10) * 10), cpu=True)
    
    def create_cpu_monitor(self):
        usage_frame = ctk.CTkFrame(self.root, corner_radius=20, width=135, height=60)
        usage_frame.place(x=self.root.winfo_width() / 2 - (usage_frame.cget("width") / 2), y=0)
        usage_frame.configure(fg_color='gray81' if self.theme == "light" else 'gray20')

        if self.theme == "light":
            images = Image.open(resource_path("CPU Dark.png", cpu=True)), Image.open(resource_path("CPU Light.png", cpu=True))
        else:
            images = Image.open(resource_path("CPU Light.png", cpu=True)), Image.open(resource_path("CPU Dark.png", cpu=True))
        
        if self.db['CPUMonitor']['dynamic_icon']:
            usage_label = ctk.CTkLabel(master=usage_frame, text=" 0.00%", text_color=self.get_color(0), image=ctk.CTkImage(Image.open(resource_path("CPU 0 - 20.png", cpu=True)), Image.open(resource_path("CPU 0 - 20.png", cpu=True)), (40, 40)), compound="left", font=("Titillium Web", 20, "bold"))
        else:
            usage_label = ctk.CTkLabel(master=usage_frame, text=" 0.00%", text_color=self.get_color(0), image=ctk.CTkImage(*images, (40, 40)), compound="left", font=("Titillium Web", 20, "bold"))
        usage_label.configure(fg_color='gray81' if self.theme == "light" else 'gray20')
        usage_label.place(x=8, y=8)

        threading.Thread(target=self.update_usage, args=(usage_label, ), daemon=True).start()

class SettingsWindow:
    def __init__(self) -> None:
        self.db = json.load(open(resource_path("config.json", data=True), "r"))
        self.example_images = json.load(open(resource_path("example_images.json", data=True), "r"))
        self.last_widget_selected_frame = None
        self.preview_class = None
    
    def on_closing(self):
        if self.preview_class:
            self.preview_class.stop()
            self.preview_class.destroy_all()
        self.root.destroy()

    def create_window(self):
        self.root = ctk.CTk()
        self.root.title("GlipseGrid")
        self.root.iconbitmap(resource_path("Icon.ico", base=True))
        self.root.geometry("600x380")
        self.root.resizable(0, 0)
        self.root._set_appearance_mode("system")
        positionRight = int(self.root.winfo_screenwidth()/2 - 600/2)
        positionDown = int(self.root.winfo_screenheight()/2 - 400/2) - 50
        self.root.geometry("+{}+{}".format(positionRight, positionDown))
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def _save(self, widgetkey, key, value):
        with open(resource_path("config.json", data=True), 'r') as f:
            d = json.load(f)
        
        if d[widgetkey][key] != value:
            d[widgetkey][key] = value

            with open(resource_path("config.json", data=True), 'w') as f:
                json.dump(d, f, indent=4)

    def _get_preview_image(self, widget: str, theme: str, info_frame: ctk.CTkFrame, start: bool = True, isdynamic: bool=True):
        if widget == "CPUMonitor":
            if start:
                if self.db[widget]['dynamic_icon']:
                    relpath = self.example_images[widget]["dynamicicon"][theme.lower()]
                else:
                    relpath = self.example_images[widget]["nodynamicicon"][theme.lower()]
            else:
                relpath = self.example_images[widget]["dynamicicon" if isdynamic else "nodynamicicon"][theme.lower()]
                
            path = resource_path(relpath, example=True)
            img = Image.open(path)
            image_size = (img.width / 1.1, img.height / 1.1)
            x = (info_frame.winfo_width() / 2) - (image_size[0] / 2)
            return img, image_size, x

    def _run_cpu_preview(self, f, d):
        self.preview_class = CPUMonitorWidget(f, d)
        self.preview_class.create_cpu_monitor()

    def show_widget_info(self, widgetkey: str, widget: str, info: ctk.CTkFrame):
        for child in info.winfo_children():
            child.destroy()
        
        def restart():
            self.root.destroy()
            app.rerun()
        
        previewLabel = ctk.CTkLabel(info, text="Preview", font=("Titillium Web", 13, "bold"))
        previewLabel.place(x=10, y=10)
        info.update()

        if widgetkey == "CPUMonitor":
            def save_callback():
                self._save(widgetkey, "status", True if status_radio_var.get() == 1 else False)
                self._save(widgetkey, "dynamic_icon", True if dyiconradio_var.get() == 1 else False)
                self._save(widgetkey, 'theme', "system" if themeradio_var.get() == 1 else "light" if themeradio_var.get() == 2 else "dark")
                restart()
            
            def on_change():
                self.preview_class.stop()
                self.preview_class.destroy_all()
                temp_db = self.db.copy()
                temp_db[widgetkey]['dynamic_icon'] = True if dyiconradio_var.get() == 1 else False
                temp_db[widgetkey]['theme'] = darkdetect.theme().lower() if themeradio_var.get() == 1 else "light" if themeradio_var.get() == 2 else "dark"
                self.preview_thread = threading.Thread(target=self._run_cpu_preview, args=(previewImageFrame, temp_db), daemon=True)
                self.preview_thread.start()

            previewImageFrame = ctk.CTkFrame(info, height=60, width=340)
            previewImageFrame.place(x=10, y=40)
            previewImageFrame.pack_propagate(0)
            self.preview_thread = threading.Thread(target=self._run_cpu_preview, args=(previewImageFrame, self.db), daemon=True)
            self.preview_thread.start()

            status_radio_var = ctk.IntVar(value=1 if self.db[widgetkey]['status'] else 0)

            ctk.CTkLabel(info, text="Widget Status", font=("Titillium Web", 13, "bold")).place(x=10, y=100)
            ctk.CTkRadioButton(info, text="ON", variable=status_radio_var, fg_color=('#008000', '#008000'), hover_color=('#008000', '#008000'), value=1).place(x=10, y=130)
            ctk.CTkRadioButton(info, text="OFF", variable=status_radio_var, fg_color=('#ff0000', '#ff0000'), hover_color=('#ff0000', '#ff0000'), value=0).place(x=160, y=130)
        
            ctk.CTkLabel(info, text="Dynamic Icon", font=("Titillium Web", 13, "bold")).place(x=10, y=160)
            dyiconradio_var = ctk.IntVar(value=1 if self.db[widgetkey]['dynamic_icon'] else 0)
            ctk.CTkRadioButton(info, text="ON", variable=dyiconradio_var, command=on_change, value=1).place(x=10, y=190)
            ctk.CTkRadioButton(info, text="OFF", variable=dyiconradio_var, command=on_change, value=0).place(x=160, y=190)
        
            ctk.CTkLabel(info, text="Theme", font=("Titillium Web", 13, "bold")).place(x=10, y=220)
            themeradio_var = ctk.IntVar(value=1 if self.db[widgetkey]['theme'] == "system" else 2 if self.db[widgetkey]['theme'] == "light" else 3 if self.db[widgetkey]['theme'] == "dark" else 0)
            ctk.CTkRadioButton(info, text="System", variable=themeradio_var, command=on_change, value=1).place(x=10, y=250)
            ctk.CTkRadioButton(info, text="Light", variable=themeradio_var, command=on_change, value=2).place(x=90, y=250)
            ctk.CTkRadioButton(info, text="Dark", variable=themeradio_var, command=on_change, value=3).place(x=170, y=250)

            save_button = ctk.CTkButton(info, text="Apply", font=("Titillium Web", 13), command=save_callback, width=50, height=20)
            save_button.place(x=info.winfo_width() - save_button.cget("width") - 10, y=info.winfo_height() - save_button.cget("height") - 15)

    def move_to_widget(self, key, widget, frame: ctk.CTkFrame, info: ctk.CTkFrame):
        if frame != self.last_widget_selected_frame:
            if self.last_widget_selected_frame:
                self.last_widget_selected_frame.configure(fg_color="transparent")
            frame.configure(fg_color=('gray81', 'gray20'))
            self.last_widget_selected_frame = frame
            self.show_widget_info(key, widget, info)
        else:
            pass

    def create_children(self):
        title = ctk.CTkLabel(self.root, text="GlimpseGrid", font=("Titillium Web", 40, "bold"))
        title.pack()

        mainFrame = ctk.CTkFrame(self.root, border_width=1, width=580, height=300)
        mainFrame.pack_propagate(0)
        mainFrame.pack()

        widgetsFrame = ctk.CTkFrame(mainFrame, width=200, height=mainFrame.cget("height") - 10, fg_color="transparent")
        widgetsFrame.pack(side="left", padx=5)
        widgetsFrame.pack_propagate(0)

        widgetinfoFrame = ctk.CTkFrame(mainFrame, width=400, height=mainFrame.cget("height") - 10, border_width=1)
        widgetinfoFrame.pack(side="right", padx=5)
        widgetinfoFrame.pack_propagate(0)

        ctk.CTkLabel(widgetinfoFrame, text="OK").place(x=10, y=10)
        widgetinfoFrame.update()

        for databasekey, widget, _, _ in widgets:
            widgetFrame = ctk.CTkFrame(widgetsFrame, width=200, height=40, fg_color="transparent", border_width=1)
            widgetFrame.pack(padx=5, pady=2, side="top")
            widgetFrame.pack_propagate(0)
            widgetFrame.bind('<Enter>', lambda e, w=widgetFrame: w.configure(cursor="hand2"))
            widgetFrame.bind('<Leave>', lambda e, w=widgetFrame: w.configure(cursor=""))
            widgetFrame.bind("<Button-1>", lambda e, wk=databasekey, w=widget, f=widgetFrame, wif=widgetinfoFrame: self.move_to_widget(wk, w, f, wif))

            widgetLabel = ctk.CTkLabel(widgetFrame, text=widget, font=("Titillium Web", 13, "bold"))
            widgetLabel.pack(anchor="center", side="left", padx=10)
            widgetLabel.bind('<Enter>', lambda e, w=widgetFrame: w.configure(cursor="hand2"))
            widgetLabel.bind('<Leave>', lambda e, w=widgetFrame: w.configure(cursor=""))
            widgetLabel.bind("<Button-1>", lambda e, wk=databasekey, w=widget, f=widgetFrame, wif=widgetinfoFrame: self.move_to_widget(wk, w, f, wif))

            statusLabel = ctk.CTkLabel(widgetFrame, text="ON" if self.db[databasekey]['status'] else "OFF", text_color="#008000" if self.db[databasekey]['status'] else "#ff0000", font=("Titillium Web", 13, "bold"))
            statusLabel.pack(anchor="center", side="right", padx=10)
            statusLabel.bind('<Enter>', lambda e, w=widgetFrame: w.configure(cursor="hand2"))
            statusLabel.bind('<Leave>', lambda e, w=widgetFrame: w.configure(cursor=""))
            statusLabel.bind("<Button-1>", lambda e, wk=databasekey, w=widget, f=widgetFrame, wif=widgetinfoFrame: self.move_to_widget(wk, w, f, wif))
            

    def run(self):
        global settingsWindow

        self.create_window()
        self.create_children()
        self.root.mainloop()

if __name__ == "__main__":
    if os.path.basename(__file__).endswith(".py"):
        app = MainPY()
        app.run()
    else:
        app = MainEXE()
        app.run()
