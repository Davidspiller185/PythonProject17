from Iwriter import IWriter
import requests


class NetworkWriter(IWriter):
    def __init__(self, base_url: str):
        self.base_url = base_url


    def send_data(self, data: str, machine_name: str) -> None:
        payload = {
            "machine_name": machine_name,
            "data": data
        }

        response = requests.post(self.base_url+"/save_data", json=payload, timeout=5)
        response.raise_for_status()


# דוגמת שימוש
if __name__ == "__main__":
    writer = NetworkWriter("https://example.com/api/data")
    writer.send_data("Hello World!", "Machine01")
