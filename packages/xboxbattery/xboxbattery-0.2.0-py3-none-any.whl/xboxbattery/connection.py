from PySide6 import QtDBus
from PySide6.QtCore import SLOT


class Connection:
    SVC = "org.freedesktop.UPower"
    PATH = "/org/freedesktop/UPower"
    INT = "org.freedesktop.UPower"
    DEV = "org.freedesktop.UPower.Device"

    dbus = QtDBus.QDBusConnection.systemBus()
    interface = QtDBus.QDBusInterface(SVC, PATH, INT, dbus)

    @classmethod
    def device(cls, path):
        return QtDBus.QDBusInterface(cls.SVC, path, cls.DEV, cls.dbus)

    @classmethod
    def connect(cls, receiver, signal, slot):
        cls.dbus.connect(cls.SVC, cls.PATH, cls.INT, signal, receiver, SLOT(slot))

    @classmethod
    def enumerate_devices(cls):
        reply = QtDBus.QDBusReply(Connection.interface.call("EnumerateDevices"))

        device_paths = []
        if reply.isValid():
            devices = reply.value()
            devices.beginArray()
            while not devices.atEnd():
                device = QtDBus.QDBusObjectPath()
                devices >> device
                device_paths.append(device.path())
            devices.endArray()

        return device_paths
