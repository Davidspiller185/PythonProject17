from Iwriter import IWriter
import os
class FileWriter(IWriter):
    def send_data(self, data: str, machine_name: str) -> None:
        """
        מקבל מחרוזת וכותב אותה לקובץ
        """
        with open(machine_name+".txt", "a", encoding="utf-8") as f:
            f.write(data)
            f.flush()  # ריקון הבאפר
            os.fsync(f.fileno())  #