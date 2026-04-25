import socket, requests, datetime, logging, json, locale, os
import pandas as pd
from pathlib import Path
from datetime import timedelta
from datetime import date
from django.core.files.storage import FileSystemStorage

try:
    locale.setlocale(locale.LC_TIME, 'id_ID.UTF-8')
except locale.Error:
    locale.setlocale(locale.LC_TIME, 'Indonesian_Indonesia.1252')

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

def baca_config():
    pathnow = Path(__file__)
    pathome = pathnow.parent
    jsonloc = pathome / 'avaro.json'

    with open(jsonloc, 'r') as file:
        return json.load(file)

def tulis_config(data):
    pathnow = Path(__file__)
    pathome = pathnow.parent
    jsonloc = pathome / 'avaro.json'

    with open(jsonloc, 'w') as file:
        json.dump(data, file, indent=4)


def data_cuaca():
    logger.info('Ambil data cuaca')
    dayNow = datetime.datetime.now()
    url = "https://api.bmkg.go.id/publik/prakiraan-cuaca?adm4=31.73.01.1003"
    dataCuaca = None
    tempList = []
    encounter = 0

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data_json = response.json()

    except requests.exceptions.HTTPError as errh:
        print(f"Http Error: {errh}")
        return False
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
        return False
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
        return False
    except requests.exceptions.RequestException as err:
        print(f"Oops: Ada yang salah: {err}")
        return False

    for loopData in data_json["data"][0]["cuaca"]:
        logger.info('Loop data cuaca')
        for getData in loopData:
            dayJson = datetime.datetime.strptime(getData["local_datetime"], "%Y-%m-%d %H:%M:%S")

            if dayJson.strftime("%Y-%m-%d") == dayNow.strftime("%Y-%m-%d"):
                tempList.append(getData['t'])
                if dayJson > dayNow and encounter == 0:
                    dataCuaca = getData
                    encounter = 1

    return data_json["data"][0]["lokasi"]["desa"], max(tempList), min(tempList), dataCuaca

# if __name__ == "__main__":
    # print(getChart1())

def getIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        s.connect(('8.8.8.8', 80))
        return s.getsockname()[0]
    except Exception:
        return '127.0.0.1'
    finally:
        s.close()

class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        # Jika file sudah ada, hapus file lama sebelum menyimpan yang baru
        if self.exists(name):
            os.remove(os.path.join(self.location, name))
        return name