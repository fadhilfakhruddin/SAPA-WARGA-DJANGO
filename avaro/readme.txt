USER	: sdapst
EMAIL	: muhfadhil.fakhrudin@artaboga.com
PASS	: Arta1234

pass gmail : zycl kyuj jyja srkq

API Gmaps
AIzaSyCN7B6kO9QJROBmWTxq_c21ZOlZzW-XHbI

Django Server
python manage.py runserver 0.0.0.0:8000

Celery Worker
--SQL Worker
celery -A avaro worker -l info --pool=threads --concurrency=4 -Q queue_vertica
--FR Worker
celery -A avaro worker -l info --pool=threads --concurrency=2 -Q queue_finereport

Celery Beat
celery -A avaro beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler

Chatery
D:\SDA\PY\chatery_whatsapp-main
npm run dev
--if conflict
taskkill /F /IM node.exe

Redis for Celery
D:\SDA\PY\Redis-x64-5.0.14.1
redis-server.exe redis.windows.conf

Perintah	Fungsi
pm2 status	Cek semua layanan
pm2 logs	Lihat log semua terminal sekaligus
pm2 monit	Dashboard CPU & RAM (Sangat bagus untuk i7 Anda)
pm2 save	Wajib dijalankan setiap kali Anda mengubah konfigurasi agar startup terupdate
pm2 restart all	Me-refresh semua layanan