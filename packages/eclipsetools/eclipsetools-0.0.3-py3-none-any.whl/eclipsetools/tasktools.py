from typing import Callable
import threading
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw


class BackgroundTask:
    def __init__(self, name: str) -> None:
        self.name = name
        self.service: BackgroundService = None

    def start(self):
        pass

    def update(self):
        pass

    def end(self):
        pass


class BackgroundService:
    def __init__(self):
        """
        Initializes the BackgroundService class and sets up the icon and processes dictionary.
        """
        self.icon = Icon("BackgroundService")
        self.names = set()
        self.threads = {}
        self.menu_items = {}

    def create_image(self, size):
        """
        Creates a simple black square image to be used as the tray icon.

        :param size: Tuple specifying the size of the icon (width, height).
        :return: A PIL Image object representing the tray icon.
        """
        image = Image.new('RGB', size, (255, 255, 255))
        dc = ImageDraw.Draw(image)
        dc.rectangle((size[0] // 4, size[1] // 4, size[0] *
                     3 // 4, size[1] * 3 // 4), fill=(0, 0, 0))
        return image

    def add_menu_item(self, name: str, task_callback: Callable, end_callback: Callable = None):
        """
        Adds a menu item to the tray menu.

        :param name: The display name of the menu item.
        :param action: The function to call when the menu item is selected.
        :return: None
        """
        item = MenuItem(f"Start {name}", lambda: self.start_task(
            name, task_callback, end_callback))
        self.menu_items[name] = item
        return item

    def add_task(self, task: BackgroundTask):
        """
        Adds a menu item to the tray menu.

        :param name: The display name of the menu item.
        :param action: The function to call when the menu item is selected.
        :return: None
        """
        item = MenuItem(f"Start {task.name}", lambda: self.start_task(
            task.name, task.start, task.update, task.end))
        self.menu_items[task.name] = item
        return item

    def start_task(self, name, start_callback: Callable = None, task_callback: Callable = None, end_callback: Callable = None):
        if self.threads.get(name, None) is None:
            thread = threading.Thread(target=lambda: self._worker(
                name, start_callback, task_callback, end_callback), daemon=True)
            self.threads[name] = thread
            self.names.add(name)
            thread.start()
            print(f"Started task [{name}]")
        else:
            print(f"Task [{name}] is already running")

    def end_task(self, name):
        thread = self.threads[name]
        if thread is None:
            print(f"No running task: [{name}]")
        else:
            self.names.remove(name)
            print(f"Closing task: [{name}] ...")

    def run(self):
        """
        Runs the system tray icon with the configured menu.

        :return: None
        """
        menu_items = []
        for item in self.menu_items:
            menu_items.append(self.menu_items[item])
            menu_items.append(
                MenuItem(f"End {item}", lambda: self.end_task(item)))
        self.icon.menu = Menu(*menu_items)
        self.icon.update_menu()
        self.icon.icon = self.create_image((64, 64))
        self.icon.run()

    def _worker(self, name, start_callback: Callable = None, task_callback: Callable = None, end_callback: Callable = None):
        if start_callback is not None:
            start_callback()
        while True:
            if not name in self.names:
                if end_callback is not None:
                    end_callback()
                    del self.threads[name]
                    print(f"Closed: [{name}]")
                return
            if start_callback is not None:
                task_callback()
