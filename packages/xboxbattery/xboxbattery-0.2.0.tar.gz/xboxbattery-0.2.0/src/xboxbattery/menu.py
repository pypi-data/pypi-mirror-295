from PySide6.QtCore import QTimer, Slot
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu

from .connection import Connection
from .device import Device


class Menu(QMenu):
    def __init__(self, parent=None):
        super().__init__()

        self.parent = parent

        self.devices = []

        self.no_devices = QAction("No devices found")
        self.quit_action = QAction("Quit")

        self.timer = QTimer()
        self.timer.timeout.connect(self.build_menu)
        self.timer.start(15000)

        Connection.connect(self, "DeviceAdded", "build_menu()")
        Connection.connect(self, "DeviceRemoved", "build_menu()")

        self.build_menu()

    @Slot()
    def build_menu(self):
        self.clear()
        self.devices.clear()

        paths = Connection.enumerate_devices()
        for path in paths:
            device = Device(path)
            self.devices.append(device)
            self.addAction(device.action)

        if not paths:
            self.no_devices.setEnabled(False)
            self.addAction(self.no_devices)

        self.addSeparator()
        self.addAction(self.quit_action)
        self.quit_action.triggered.connect(self.parent.quit)
