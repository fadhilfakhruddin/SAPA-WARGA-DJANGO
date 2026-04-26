from django.db import models
import uuid, os
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.utils import timezone

class ListBlok(models.Model):
    blok = models.CharField(max_length=100, blank=False, null=False, primary_key=True)
    nama_blok = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return f"{self.blok} - {self.nama_blok}"

class Profile(models.Model):
    STATUS_CHOICES = [
        ('belum_kawin', 'Belum Kawin'),
        ('kawin', 'Kawin'),
    ]

    enambelas_digit_validator = RegexValidator(
        regex=r'^\d{16}$',
        message='Data harus terdiri dari tepat 16 digit angka.'
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nik_kepala = models.CharField(max_length=16, validators=[enambelas_digit_validator], blank=True, null=True)
    nama_kepala = models.CharField(max_length=100, blank=True, null=True)
    nik_pasangan = models.CharField(max_length=16, validators=[enambelas_digit_validator], blank=True, null=True)
    nama_pasangan = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='belum_kawin')
    jumlah_penghuni = models.IntegerField(blank=True, null=True)
    kartu_keluarga = models.CharField(max_length=16, validators=[enambelas_digit_validator], blank=True, null=True)
    blok = models.ForeignKey(ListBlok, on_delete=models.CASCADE, null=True, blank=True)
    asal_daerah = models.TextField(blank=True, null=True)
    phone_number = PhoneNumberField(null=True, blank=True, region="ID")

    def __str__(self):
        return f'{self.user.username} Profile'

def rename_bukti_transaksi(instance, filename):
    """
    Format nama file: bukti_transaksi/bukti_{uuid_acak}.{ekstensi_asli}
    """
    ext = filename.split('.')[-1]
    
    unique_id = uuid.uuid4().hex[:8]
    
    new_filename = f"bukti_{unique_id}.{ext}"
    
    return os.path.join('bukti_transaksi/', new_filename)
    
class Transaksi(models.Model):
    JENIS_TRANSAKSI = [
        ('debit', 'Debit'),
        ('kredit', 'Kredit')
    ]

    tanggal = models.DateField(default=timezone.now)
    jenis = models.CharField(max_length=10, choices=JENIS_TRANSAKSI)
    kategori = models.CharField(max_length=100)
    nominal = models.DecimalField(max_digits=12, decimal_places=2)
    keterangan = models.TextField(blank=True, null=True)
    
    warga = models.ForeignKey('Profile', on_delete=models.SET_NULL, null=True, blank=True)
    bukti_transaksi = models.ImageField(upload_to=rename_bukti_transaksi, blank=True, null=True)

    user_input = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='transaksi_dicatat')
    tanggal_input = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.tanggal} - {self.get_jenis_display()} - Rp{self.nominal}"