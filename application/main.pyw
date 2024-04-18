import threading
import os
from PIL import Image
import sys
import customtkinter as ctk
import pystray
import subprocess
import os
import time

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

widgetsPY = [
    ["CPU Widget", "application/cpu.pyw"],
    ["Network Widget", "application/network.pyw"]
]
widgetsEXE = [
    ["CPU Widget", "CPU Widget.exe"],
    ["Network Widget", "Network Widget.exe"]
]

class MainEXE:
    def __init__(self) -> None:
        self.running_processes = {}

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
                pystray.MenuItem('Show', self.default_function, default=True),
                pystray.MenuItem("Close",  self.generate_submenu(False)),
                pystray.MenuItem('Close All', self.exit_action)
            )
            icon.update_menu()
    
    def exit_action(self, icon, item) -> None:
        for process_name in self.running_processes:
            self.running_processes[process_name].terminate()
        icon.stop()
        os._exit(0)

    def default_function(self, icon, item):
        print("Nice!", item)
    
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
                pystray.MenuItem('Show', self.default_function, default=True),
                pystray.MenuItem("Close",  self.generate_submenu()),
                pystray.MenuItem('Close All', self.exit_action)
                )
        )
        icon.run()
    
    def run(self):
        for process_name, script_path in widgetsEXE:
            threading.Thread(target=self._run_script, args=(process_name, script_path, ), daemon=True).start()
        self.run_on_systray()
    

class MainPY:
    def __init__(self) -> None:
        self.running_processes = {}

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
                pystray.MenuItem('Show', self.default_function, default=True),
                pystray.MenuItem("Close",  self.generate_submenu(False)),
                pystray.MenuItem('Close All', self.exit_action)
            )
            icon.update_menu()
    
    def exit_action(self, icon, item) -> None:
        for process_name in self.running_processes:
            self.running_processes[process_name].terminate()
        icon.stop()
        os._exit(0)

    def default_function(self, icon, item):
        print("Nice!", item)
    
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
                pystray.MenuItem('Show', self.default_function, default=True),
                pystray.MenuItem("Close",  self.generate_submenu()),
                pystray.MenuItem('Close All', self.exit_action)
                )
        )
        icon.run()
    
    def run(self):
        for process_name, script_path in widgetsPY:
            threading.Thread(target=self._run_script, args=(process_name, script_path, ), daemon=True).start()
        self.run_on_systray()

if __name__ == "__main__":
    if os.path.basename(__file__).endswith(".py"):
        app = MainEXE()
        app.run()
