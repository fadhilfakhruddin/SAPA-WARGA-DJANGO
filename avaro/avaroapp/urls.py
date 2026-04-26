from django.urls import path
from . import views

urlpatterns = [
    path('', views.avaroapp, name='avaroapp'),
    path('daftar-blok/', views.daftarBlok, name='daftar_blok'),
    path('del-blok/<str:blok_id>/', views.del_blok, name='del_blok'),
    path('edit-blok/<str:blok_id>/', views.edit_blok, name='edit_blok'),

    path('daftar-warga/', views.daftarkan_warga, name='daftarkan_warga'),
    path('edit-warga/<str:username>/', views.edit_warga, name='edit_warga'),
    path('del-warga/<str:username>/', views.del_warga, name='del_warga'),

    path('ganti-password/', views.ganti_password, name='ganti_password'),
    path('reset-password-default/<str:username>/', views.reset_password_default, name='reset_password_default'),

    path('transaksi/', views.daftar_transaksi, name='daftar_transaksi'),
    path('del-transaksi/<int:id_transaksi>/', views.del_transaksi, name='del_transaksi'),

    path('rekap-pemasukan/', views.rekap_pemasukan, name='rekap_pemasukan'),
    path('rekap-kas/', views.rekap_kas, name='rekap_kas'),

    path('profile/', views.profile_view, name='profile'),
]