from server.agent.Iwriter import IWriter
import os


class FileWriter(IWriter):
    def send_data(self, data: str, machine_name: str) -> None:
        """
        מקבל מחרוזת וכותב אותה לקובץ
        """
        # date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        # time_str = datetime.datetime.now().strftime("%H:%M:%S")
        filename = machine_name + ".txt"

        with open(filename, "a", encoding="utf-8") as f:
            f.write(data)
            f.flush()  # ריקון הבאפר
            os.fsync(f.fileno())  #

