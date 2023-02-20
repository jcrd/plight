import logging

from gi.repository import Gio, GLib

LOGIND_NAME = "org.freedesktop.login1"
LOGIND_IFACE = f"{LOGIND_NAME}.Session"
LOGIND_PATH = "/org/freedesktop/login1/session/auto"


class Logind:
    def __init__(self, wakeup_callback):
        def on_logind_signal(self, conn, sender, signal, args):
            if signal != "PrepareForSleep":
                return
            if args.unpack()[0] == False:
                logging.debug("Logind: waking up")
                wakeup_callback()

        self.logind = Gio.DBusProxy.new_sync(
            Gio.bus_get_sync(Gio.BusType.SYSTEM, None),
            Gio.DBusProxyFlags.NONE,
            None,
            LOGIND_NAME,
            LOGIND_PATH,
            LOGIND_IFACE,
            None,
        )
        self.logind.connect("g-signal", on_logind_signal)

    def set_brightness(self, name, v):
        var = GLib.Variant("(ssu)", ("backlight", name, v))
        self.logind.call_sync(
            "SetBrightness", var, Gio.DBusCallFlags.NO_AUTO_START, 3000, None
        )
