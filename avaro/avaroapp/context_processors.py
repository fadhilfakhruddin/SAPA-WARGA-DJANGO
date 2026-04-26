from .models import Transaksi
from django.db.models.functions import ExtractYear

def list_tahun(request):
    listTahun = Transaksi.objects.annotate(
        tahun=ExtractYear('tanggal')
    ).values_list('tahun', flat=True).distinct()

    return {'list_tahun' : listTahun}