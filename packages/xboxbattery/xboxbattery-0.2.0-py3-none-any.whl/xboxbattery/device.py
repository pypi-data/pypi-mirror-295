import glob
import subprocess

from PySide6.QtCore import QTimer
from PySide6.QtGui import QAction

from .connection import Connection


class Device:
    def __init__(self, path):
        self.path = path
        self.gip = self.path.split("/")[-1].split("_")[-1].replace("x", ".")
        self.interface = Connection.device(self.path)

        self.model = self.interface.property("Model")
        self.percentage = self.interface.property("Percentage")

        self.action = QAction(f"{self.model} ({self.percentage}%)")
        self.action.triggered.connect(self.blink_led)

    def blink_led(self):
        self.set_led(3)
        QTimer.singleShot(3000, lambda: self.set_led(1))

    def set_led(self, signal):
        targets = glob.glob(f"/sys/class/leds/{self.gip}:*:status/mode")
        for target in targets:
            subprocess.Popen(f"echo {signal} > {target}", shell=True)
