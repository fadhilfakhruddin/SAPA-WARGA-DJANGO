from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, ListBlok, Transaksi
from urllib.parse import urlparse
import re, json
from django.db.models import Q

class DaftarBlokForm(forms.ModelForm):
    class Meta:
        model = ListBlok
        fields = ['blok', 'nama_blok']
        labels = {
            'blok' : 'Kode Blok',
            'nama_blok' : 'Nama Blok',
        }
        widgets = {
            'blok': forms.TextInput(attrs={
                'placeholder': 'Masukkan Kode Blok'
            }),
            'nama_blok': forms.TextInput(attrs={
                'placeholder': 'Masukkan Nama Blok'
            })
        }

class PendaftaranWargaForm(forms.Form):
    blok = forms.ModelChoiceField(
        queryset=ListBlok.objects.all(), 
        label="Pilih Blok Rumah", 
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    nama_kepala = forms.CharField(
        max_length=100, 
        label="Nama Kepala Keluarga", 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan nama'})
    )

    email = forms.EmailField(
        max_length=100, 
        label="Email (Opsional)",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan Alamat Email'})
    )

    phone_number = forms.CharField(
        max_length=20, 
        label="Nomor WhatsApp (Opsional)", 
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Contoh: 081234567890',
            'type': 'tel'
        })
    )

class UserUpdateForm(forms.ModelForm):
    """Form untuk mengedit info dasar User."""
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    """Form untuk mengedit info tambahan di Profile."""
    class Meta:
        model = Profile
        fields = ['nik_kepala', 'nama_kepala', 'nik_pasangan', 'nama_pasangan', 'status', 'jumlah_penghuni', 'kartu_keluarga', 'blok', 'no_rumah', 'asal_daerah', 'phone_number']
        labels = {
            'nik_kepala' : 'NIK Kepala Keluarga',
            'nama_kepala' : 'Nama Kepala Keluarga',
            'nik_pasangan' : 'NIK Pasangan',
            'nama_pasangan' : 'Nama Pasangan',
            'jumlah_penghuni' : 'Jumlah Penghuni',
            'kartu_keluarga' : 'No. KK',
            'asal_daerah' : 'Asal Daerah',
            'phone_number' : 'No. Telp',
            'no_rumah' : 'Nomor Rumah',
        }
        widgets = {
            'nama_kepala': forms.TextInput(attrs={
                'placeholder': 'Masukkan nama lengkap'
            }),
            'nama_pasangan': forms.TextInput(attrs={
                'placeholder': 'Masukkan nama lengkap'
            }),
            'phone_number': forms.TextInput(attrs={
                'placeholder': '0812xxxx atau +62812xxxx'
            }),
        }

class TransaksiForm(forms.ModelForm):
    class Meta:
        model = Transaksi
        fields = ['tanggal', 'jenis', 'warga', 'nominal', 'keterangan', 'bukti_transaksi']
        widgets = {
            'tanggal': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'keterangan': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Opsional...'}),
            'jenis': forms.Select(attrs={'class': 'form-select'}),
            'warga': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'warga': 'Pilih Warga',
            'bukti_transaksi': 'Upload Bukti (Opsional)'
        }