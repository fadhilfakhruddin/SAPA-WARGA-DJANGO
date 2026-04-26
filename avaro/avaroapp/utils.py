import socket, requests, datetime, logging, json, locale, os
import pandas as pd
from pathlib import Path
from .models import Transaksi

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

def data_kas(tahun):
    list_bulan = list(range(1, 13))

    rekap_bulanan = {
        'pemasukan': {m: 0 for m in list_bulan},
        'pengeluaran': {m: 0 for m in list_bulan},
        'saldo': {m: 0 for m in list_bulan},
        'total_pemasukan': 0,
        'total_pengeluaran': 0,
        'total_saldo': 0
    }

    transaksi = Transaksi.objects.filter(tanggal__year=tahun)

    for tx in transaksi:
        bulan_tx = tx.tanggal.month
        if tx.jenis == 'debit':
            rekap_bulanan['pemasukan'][bulan_tx] += tx.nominal
            rekap_bulanan['total_pemasukan'] += tx.nominal
        elif tx.jenis == 'kredit': # Sesuaikan dengan value 'kredit' di models.py Anda
            rekap_bulanan['pengeluaran'][bulan_tx] += tx.nominal
            rekap_bulanan['total_pengeluaran'] += tx.nominal

        for m in list_bulan:
            rekap_bulanan['saldo'][m] = rekap_bulanan['pemasukan'][m] - rekap_bulanan['pengeluaran'][m]
        rekap_bulanan['total_saldo'] = rekap_bulanan['total_pemasukan'] - rekap_bulanan['total_pengeluaran']

    return rekap_bulanan

# if __name__ == "__main__":
    # print(getChart1())