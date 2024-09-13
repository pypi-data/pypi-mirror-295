from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QSystemTrayIcon

from .menu import Menu


class App(QApplication):
    def __init__(self):
        super().__init__()
        self.tray = QSystemTrayIcon()

        self.icon = QIcon.fromTheme(QIcon.ThemeIcon.InputGaming)
        self.tray.setIcon(self.icon)
        self.tray.setVisible(True)

        self.menu = Menu(self)
        self.tray.setContextMenu(self.menu)


def main():
    app = App()
    app.exec()
