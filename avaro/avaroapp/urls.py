from django.urls import path, include
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
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

    # CHATERY
    # path('webhook/chatery/', views.chatery_webhook, name='chatery_webhook'),
    # path('send-document/', views.API_send_document, name='send_document'),
    # path('send-image/', views.API_send_image, name='send_image'),

    path('profile/', views.profile_view, name='profile'),
]

# if settings.DEBUG:
#     urlpatterns += static('/hasil-excel/', document_root=settings.EXCEL_RESULTS_ROOT)
#     # Jika Anda masih pakai media biasa, biarkan yang ini tetap ada
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)