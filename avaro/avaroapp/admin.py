from django.contrib import admin

from .models import Profile, ListBlok, Transaksi

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','nama_kepala','status','phone_number')
    search_fields = ('user','nama_kepala','status','phone_number')

@admin.register(ListBlok)
class ListBlokAdmin(admin.ModelAdmin):
    list_display = ('blok','nama_blok')
    search_fields = ('blok','nama_blok')

@admin.register(Transaksi)
class TransaksiAdmin(admin.ModelAdmin):
    list_display = ('tanggal','jenis','nominal','keterangan','user_input','tanggal_input')
    search_fields = ('tanggal','jenis','nominal','keterangan','user_input','tanggal_input')