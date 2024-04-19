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
import ast

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


class SettingsWindow:
    def __init__(self) -> None:
        self.db = json.load(open(resource_path("config.json", data=True), "r"))
        self.settings_design = json.load(open(resource_path("settings.json", data=True), "r"))
        self.example_images = json.load(open(resource_path("example_images.json", data=True), "r"))
        self.last_widget_selected_frame = None

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
    
    def _save(self, widgetkey, key, value):
        with open(resource_path("config.json", data=True), 'r') as f:
            d = json.load(f)
        
        if d[widgetkey][key] != value:
            d[widgetkey][key] = value

            with open(resource_path("config.json", data=True), 'w') as f:
                json.dump(d, f, indent=4)

            self.root.destroy()
            app.rerun()

    def _get_preview_image(self, widget: str, theme: str, start: bool = True, isdynamic: bool=True):
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
            return img, (img.width / 1.1, img.height / 1.1)

    def show_widget_info(self, widgetkey: str, widget: str, info: ctk.CTkFrame):
        for child in info.winfo_children():
            child.destroy()
        
        previewLabel = ctk.CTkLabel(info, text="Preview", font=("Titillium Web", 13, "bold"))
        previewLabel.pack(pady=5, padx=10, anchor="nw")
        info.update()
        preview_image, size = self._get_preview_image(widgetkey, darkdetect.theme())
        previewImageLabel = ctk.CTkLabel(info, text="", image=ctk.CTkImage(preview_image, preview_image, (size)))
        previewImageLabel.pack(anchor="center")
        status_radio_var = ctk.IntVar(value=1 if self.db[widgetkey]['status'] else 0)

        def save_callback():
            self._save(widgetkey, "status", True if status_radio_var.get() == 1 else False)
            self._save(widgetkey, "dynamic_icon", True if dyiconradio_var.get() == 1 else False)

        def on_change():
            if dyiconradio_var.get() == 0:
                preview_image, size = self._get_preview_image(widgetkey, darkdetect.theme(), False, False)
                previewImageLabel.configure(image=ctk.CTkImage(preview_image, preview_image, (size)))
            else:
                preview_image, size = self._get_preview_image(widgetkey, darkdetect.theme(), False, True)
                previewImageLabel.configure(image=ctk.CTkImage(preview_image, preview_image, (size)))

        if widgetkey == "CPUMonitor":
            ctk.CTkLabel(info, text="Widget Status", font=("Titillium Web", 13, "bold")).place(x=10, y=100)
            ctk.CTkRadioButton(info, text="ON", variable=status_radio_var, fg_color=('#008000', '#008000'), hover_color=('#008000', '#008000'), value=1).place(x=10, y=130)
            ctk.CTkRadioButton(info, text="OFF", variable=status_radio_var, fg_color=('#ff0000', '#ff0000'), hover_color=('#ff0000', '#ff0000'), value=0).place(x=160, y=130)
        
            ctk.CTkLabel(info, text="Dynamic Icon", font=("Titillium Web", 13, "bold")).place(x=10, y=170)
            dyiconradio_var = ctk.IntVar(value=1 if self.db[widgetkey]['dynamic_icon'] else 0)
            ctk.CTkRadioButton(info, text="ON", variable=dyiconradio_var, command=on_change, value=1).place(x=10, y=200)
            ctk.CTkRadioButton(info, text="OFF", variable=dyiconradio_var, command=on_change, value=0).place(x=160, y=200)

            save_button = ctk.CTkButton(info, text="Apply", font=("Titillium Web", 13), command=save_callback, width=50, height=20)
            save_button.pack(padx=10, pady=20, anchor="se", side="bottom") 

    def move_to_widget(self, key, widget, frame: ctk.CTkFrame, info: ctk.CTkFrame):
        if frame != self.last_widget_selected_frame:
            if self.last_widget_selected_frame:
                self.last_widget_selected_frame.configure(fg_color="transparent")
            frame.configure(fg_color=('gray81', 'gray20'))
            self.last_widget_selected_frame = frame
            print(key)
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

        widgetinfoFrame = ctk.CTkFrame(mainFrame, width=400, height=mainFrame.cget("height") - 10, fg_color="transparent", border_width=1)
        widgetinfoFrame.pack(side="right", padx=5)
        widgetinfoFrame.pack_propagate(0)

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
