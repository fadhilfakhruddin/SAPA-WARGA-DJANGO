from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import PendaftaranWargaForm, UserUpdateForm, ProfileUpdateForm, DaftarBlokForm, TransaksiForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.db import transaction
from django.conf import settings
from django.core.cache import cache
from .models import Profile, ListBlok, Transaksi
from django.db.models import Sum
import locale, re, calendar
from django.utils import timezone
from .utils import data_kas

try:
    locale.setlocale(locale.LC_TIME, 'id_ID.UTF-8')
except locale.Error:
    locale.setlocale(locale.LC_TIME, 'Indonesian_Indonesia.1252')

import logging
logger = logging.getLogger(__name__)


@login_required
def avaroapp(request):
    sekarang = timezone.localtime(timezone.now())
    tahun_sekarang = sekarang.year
    bulan_sekarang = sekarang.month
    semua_transaksi = Transaksi.objects.select_related('warga', 'user_input').order_by('-tanggal').all()

    pemasukan_total_sekarang = semua_transaksi.filter(jenis='debit').aggregate(total=Sum('nominal'))['total'] or 0
    pengeluaran_total_sekarang = semua_transaksi.filter(jenis='kredit').aggregate(total=Sum('nominal'))['total'] or 0
    saldo_sekarang = pemasukan_total_sekarang - pengeluaran_total_sekarang

    pemasukan_total_lalu = semua_transaksi.filter(jenis='debit').exclude(tanggal__year=tahun_sekarang, tanggal__month=bulan_sekarang).aggregate(total=Sum('nominal'))['total'] or 0
    pengeluaran_total_lalu = semua_transaksi.filter(jenis='kredit').exclude(tanggal__year=tahun_sekarang, tanggal__month=bulan_sekarang).aggregate(total=Sum('nominal'))['total'] or 0
    saldo_lalu = pemasukan_total_lalu - pengeluaran_total_lalu    

    transaksi_sekarang = semua_transaksi.filter(tanggal__year=tahun_sekarang, tanggal__month=bulan_sekarang)
    pemasukan_sekarang = transaksi_sekarang.filter(jenis='debit').aggregate(total=Sum('nominal'))['total'] or 0
    pengeluaran_sekarang = transaksi_sekarang.filter(jenis='kredit').aggregate(total=Sum('nominal'))['total'] or 0

    list_warga = Profile.objects.all()
    list_warga_sekarang = transaksi_sekarang.filter(jenis='debit').values('warga').distinct()

    transaksi_user = transaksi_sekarang.filter(warga=request.user.profile)
    pemasukan_user = transaksi_user.filter(jenis='debit').aggregate(total=Sum('nominal'))['total'] or 0

    rekap_bulanan = data_kas(tahun_sekarang)

    context = {
        'active_page' : 'dashboard',
        'daftar_transaksi' : semua_transaksi[:5],
        'saldo' : saldo_sekarang,
        'trend' : saldo_sekarang - saldo_lalu,
        'warga_bayar' : list_warga_sekarang.count(),
        'jml_warga' : list_warga.count(),
        'pemasukan' : pemasukan_sekarang,
        'pengeluaran' : pengeluaran_sekarang,
        'pemasukan_user' : pemasukan_user,
        'rekap_bulanan' : rekap_bulanan,
        'tahun_sekarang' : tahun_sekarang,
    }
    return render(request, 'index_base.html', context)

def daftarkan_warga(request):
    daftar_warga = Profile.objects.all().order_by('blok','nama_kepala')

    if request.method == 'POST':
        form = PendaftaranWargaForm(request.POST)
        if form.is_valid():
            blok = form.cleaned_data['blok']
            nama = form.cleaned_data['nama_kepala']

            email_user = form.cleaned_data.get('email')
            phone_number = form.cleaned_data.get('phone_number')


            clean_blok = re.sub(r'\s+', '', blok.blok).lower()
            clean_nama = re.sub(r'\s+', '', nama).lower()
            username = f"{clean_blok}_{clean_nama}"

            if User.objects.filter(username=username).exists():
                messages.error(request, f"Gagal: Username '{username}' sudah digunakan.")
            else:
                default_password = 'SapaWarga123'
                user = User.objects.create_user(
                    username=username,
                    password=default_password,
                )

                if email_user:
                    user.email = email_user

                profile = user.profile
                profile.blok = blok
                profile.nama_kepala = nama
                if phone_number:
                    profile.phone_number = phone_number
                profile.save()

                pesan_sukses = f"Berhasil! Akun warga dibuat. Username: {username} | Password: {default_password}"
                messages.success(request, pesan_sukses)
                
                return redirect('daftarkan_warga') 
    else:
        form = PendaftaranWargaForm()

    context = {
        'active_page': 'daftarWarga',
        'form': form,
        'daftar_warga' : daftar_warga
    }
    return render(request, 'daftar-warga.html', context)

@login_required
@transaction.atomic 
def profile_view(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profil Anda berhasil diperbarui.')
            return redirect('profile')
        else:
            messages.error(request, 'Terjadi kesalahan. Harap periksa data Anda.')
            
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'active_page': 'profile'
    }
    return render(request, 'profile.html', context)

@login_required
def edit_warga(request, username):
    if not request.user.is_superuser:
        messages.error(request, "Akses ditolak! Anda tidak memiliki izin mengedit data warga lain.")
        return redirect('daftarkan_warga')

    target_user = get_object_or_404(User, username=username)
    target_profile = target_user.profile

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=target_user)
        profile_form = ProfileUpdateForm(request.POST, instance=target_profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f"Data warga {target_profile.nama_kepala} berhasil diperbarui!")
            
            return redirect('daftarkan_warga') 
        else:
            messages.error(request, "Gagal memperbarui data. Silakan periksa kembali form.")
    else:
        user_form = UserUpdateForm(instance=target_user)
        profile_form = ProfileUpdateForm(instance=target_profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'target_user': target_user 
    }
    return render(request, 'profile.html', context)

@login_required
def del_warga(request, username):
    if not request.user.is_superuser:
        messages.error(request, "Akses ditolak! Anda tidak memiliki izin untuk menghapus data warga.")
        return redirect('daftarkan_warga')

    if request.user.username == username:
        messages.error(request, "Peringatan: Anda tidak dapat menghapus akun admin Anda sendiri!")
        return redirect('daftarkan_warga')

    target_user = get_object_or_404(User, username=username)
    
    nama_warga = target_user.profile.nama_kepala or target_user.username

    try:
        target_user.delete()
        messages.success(request, f"Data warga {nama_warga} beserta akun login-nya berhasil dihapus permanen!")
    except Exception as e:
        messages.error(request, "Terjadi kesalahan saat menghapus data warga.")
        
    return redirect('daftarkan_warga')

@login_required
def ganti_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  
            messages.success(request, 'Password Anda berhasil diperbarui!')
            
            return redirect('profile') 
        else:
            messages.error(request, 'Gagal mengganti password. Silakan periksa kembali form di bawah.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'ganti-password.html', {'form': form})

@login_required
def reset_password_default(request, username):
    if not request.user.is_superuser:
        messages.error(request, "Akses ditolak! Hanya admin yang dapat mereset password warga.")
        return redirect('daftarkan_warga')

    target_user = get_object_or_404(User, username=username)
    
    try:
        target_user.set_password('SapaWarga123')
        target_user.save()
        messages.success(request, f"Password untuk warga '{target_user.username}' berhasil direset menjadi 'SapaWarga123'.")
    except Exception as e:
        messages.error(request, "Terjadi kesalahan saat mereset password.")
    
    return redirect('daftarkan_warga')


@login_required
def daftarBlok(request):
    if not request.user.is_superuser or not request.user.is_staff:
        messages.error(request, "Anda tidak memiliki akses ke halaman ini.")
        return redirect('avaroapp')
    
    if request.method == 'POST':
        form = DaftarBlokForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data blok berhasil ditambahkan!')
        else:
            messages.error(request, 'Terjadi kesalahan. Harap periksa data Anda.')
    else:
        form = DaftarBlokForm()

    daftar_blok = ListBlok.objects.all().order_by('blok')

    context = {
        'active_page': 'daftarBlok',
        'form': form,
        'daftarBlok' : daftar_blok,
    }
    return render(request, 'daftar-blok.html', context)

@login_required
def del_blok(request, blok_id):

    blok = get_object_or_404(ListBlok, blok=blok_id)
    base_url = request.GET.get('next')

    try:
        blok.delete()
        messages.success(request, 'Blok Berhasil Dihapus!')

        return redirect(base_url)
    except:
        messages.error(request, 'Gagal Menghapus Blok')
        return redirect(base_url)

@login_required
def edit_blok(request, blok_id):

    blok = get_object_or_404(ListBlok, blok=blok_id)
    base_url = request.GET.get('next')

    try:
        if request.method == "POST":
            nama_blok_new = request.POST.get('nama_blok')
            blok.nama_blok = nama_blok_new

            blok.save()
            messages.success(request,  f'Blok {blok.blok} berhasil diperbarui!')

        return redirect(base_url)
    except:
        messages.error(request, 'Gagal Menghapus Blok')
        return redirect(base_url)

def daftar_transaksi(request):
    filter_jenis = request.GET.get('jenis')
    filter_bulan = request.GET.get('bulan')
    filter_tahun = request.GET.get('tahun')

    semua_transaksi = Transaksi.objects.select_related('warga', 'user_input').all()

    if filter_jenis:
        semua_transaksi = semua_transaksi.filter(jenis=filter_jenis)
    if filter_bulan:
        semua_transaksi = semua_transaksi.filter(tanggal__month=filter_bulan)
    if filter_tahun:
        semua_transaksi = semua_transaksi.filter(tanggal__year=filter_tahun)
        
    semua_transaksi = semua_transaksi.order_by('-tanggal', '-id')
    
    form = TransaksiForm()

    if request.method == 'POST':
        if not request.user.is_superuser:
            messages.error(request, "Akses ditolak! Anda tidak dapat menginput transaksi.")
            return redirect('daftar_transaksi')
        
        form = TransaksiForm(request.POST, request.FILES)
        
        if form.is_valid():
            transaksi_baru = form.save(commit=False)
            transaksi_baru.user_input = request.user
            transaksi_baru.save()
            
            messages.success(request, f"Berhasil! Transaksi senilai Rp {transaksi_baru.nominal} telah dicatat.")
            return redirect('daftar_transaksi')
        else:
            messages.error(request, "Gagal mencatat transaksi. Periksa kembali form isian.")

    context = {
        'active_page': 'daftarTransaksi',
        'daftar_transaksi': semua_transaksi,
        'form': form
    }
    return render(request, 'daftar-transaksi.html', context)

@login_required
def del_transaksi(request, id_transaksi):
    data_transaksi = Transaksi.objects.filter(id=id_transaksi).first()

    try:
        data_transaksi.delete()
        messages.success(request, 'Transaksi berhasil dihapus!')
    except:
        messages.error(request, 'Gagal menghapus transaksi')
    
    return redirect('daftar_transaksi')

@login_required
def rekap_pemasukan(request):
    sekarang = timezone.localtime(timezone.now())
    mode = request.GET.get('mode', 'bulanan') 
    
    tahun = int(request.GET.get('tahun', sekarang.year))
    bulan = int(request.GET.get('bulan', sekarang.month))
    
    warga_list = Profile.objects.select_related('blok').all().order_by('blok__blok')
    
    rekap_bulanan = []
    rekap_harian = []
    list_bulan = list(range(1, 13))
    list_hari = []

    if mode == 'bulanan':
        transaksi = Transaksi.objects.filter(jenis='debit', tanggal__year=tahun)
        
        for w in warga_list:
            rekap_bulanan.append({
                'warga': w,
                'bulan': {m: 0 for m in list_bulan},
                'total': 0
            })
            
        warga_map = {d['warga'].id: d for d in rekap_bulanan}
        
        for tx in transaksi:
            if tx.warga_id in warga_map:
                warga_map[tx.warga_id]['bulan'][tx.tanggal.month] += tx.nominal
                warga_map[tx.warga_id]['total'] += tx.nominal

    elif mode == 'harian':
        _, num_days = calendar.monthrange(tahun, bulan)
        list_hari = list(range(1, num_days + 1))
        
        transaksi = Transaksi.objects.filter(jenis='debit', tanggal__year=tahun, tanggal__month=bulan)
        
        for w in warga_list:
            rekap_harian.append({
                'warga': w,
                'hari': {d: 0 for d in list_hari},
                'total': 0
            })
            
        warga_map = {d['warga'].id: d for d in rekap_harian}
        
        for tx in transaksi:
            if tx.warga_id in warga_map:
                warga_map[tx.warga_id]['hari'][tx.tanggal.day] += tx.nominal
                warga_map[tx.warga_id]['total'] += tx.nominal

    context = {
        'active_page': 'rekapPemasukan',
        'mode': mode,
        'tahun': tahun,
        'bulan': bulan,
        'list_bulan': list_bulan,
        'list_hari': list_hari,
        'rekap_bulanan': rekap_bulanan,
        'rekap_harian': rekap_harian,
    }
    return render(request, 'rekap-pemasukan.html', context)

@login_required
def rekap_kas(request):
    sekarang = timezone.localtime(timezone.now())
    mode = request.GET.get('mode', 'bulanan') 
    
    tahun = int(request.GET.get('tahun', sekarang.year))
    bulan = int(request.GET.get('bulan', sekarang.month))
    
    list_bulan = list(range(1, 13))
    list_hari = []
    
    rekap_bulanan = {
        'pemasukan': {m: 0 for m in list_bulan},
        'pengeluaran': {m: 0 for m in list_bulan},
        'saldo': {m: 0 for m in list_bulan},
        'total_pemasukan': 0,
        'total_pengeluaran': 0,
        'total_saldo': 0
    }
    
    rekap_harian = {} 

    if mode == 'bulanan':
        transaksi = Transaksi.objects.filter(tanggal__year=tahun)
        
        for tx in transaksi:
            bulan_tx = tx.tanggal.month
            if tx.jenis == 'debit':
                rekap_bulanan['pemasukan'][bulan_tx] += tx.nominal
                rekap_bulanan['total_pemasukan'] += tx.nominal
            elif tx.jenis == 'kredit': 
                rekap_bulanan['pengeluaran'][bulan_tx] += tx.nominal
                rekap_bulanan['total_pengeluaran'] += tx.nominal
                
        for m in list_bulan:
            rekap_bulanan['saldo'][m] = rekap_bulanan['pemasukan'][m] - rekap_bulanan['pengeluaran'][m]
        rekap_bulanan['total_saldo'] = rekap_bulanan['total_pemasukan'] - rekap_bulanan['total_pengeluaran']

    elif mode == 'harian':
        _, num_days = calendar.monthrange(tahun, bulan)
        list_hari = list(range(1, num_days + 1))
        
        rekap_harian = {
            'pemasukan': {d: 0 for d in list_hari},
            'pengeluaran': {d: 0 for d in list_hari},
            'saldo': {d: 0 for d in list_hari},
            'total_pemasukan': 0,
            'total_pengeluaran': 0,
            'total_saldo': 0
        }
        
        transaksi = Transaksi.objects.filter(tanggal__year=tahun, tanggal__month=bulan)
        
        for tx in transaksi:
            hari_tx = tx.tanggal.day
            if tx.jenis == 'debit':
                rekap_harian['pemasukan'][hari_tx] += tx.nominal
                rekap_harian['total_pemasukan'] += tx.nominal
            elif tx.jenis == 'kredit':
                rekap_harian['pengeluaran'][hari_tx] += tx.nominal
                rekap_harian['total_pengeluaran'] += tx.nominal
                
        for d in list_hari:
            rekap_harian['saldo'][d] = rekap_harian['pemasukan'][d] - rekap_harian['pengeluaran'][d]
        rekap_harian['total_saldo'] = rekap_harian['total_pemasukan'] - rekap_harian['total_pengeluaran']

    context = {
        'active_page': 'rekapKas',
        'mode': mode,
        'tahun': tahun,
        'bulan': bulan,
        'list_bulan': list_bulan,
        'list_hari': list_hari,
        'rekap_bulanan': rekap_bulanan,
        'rekap_harian': rekap_harian,
    }
    return render(request, 'rekap-kas.html', context)