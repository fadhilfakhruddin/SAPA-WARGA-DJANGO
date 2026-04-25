from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Sinyal ini dipanggil setiap kali objek User disimpan.
    Ini akan membuat Profile jika belum ada.
    """
    if created:
        # Jika user BARU dibuat, buat profile untuknya.
        Profile.objects.create(user=instance)
    else:
        # Jika user LAMA disimpan (misal: superuser login)
        # Cek apakah dia punya profil.
        if not hasattr(instance, 'profile'):
            # Jika tidak punya (ini kasus superuser Anda), BUATKAN.
            Profile.objects.create(user=instance)
        else:
            # Jika dia punya, simpan saja (ini untuk user biasa)
            instance.profile.save()

