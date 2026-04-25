import os
import sys
from waitress import serve
from django.core.wsgi import get_wsgi_application
# from dj_static import Cling, MediaCling

sys.path.append(os.getcwd())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'avaro.settings')

# application = MediaCling(Cling(get_wsgi_application()))
application = get_wsgi_application()

if __name__ == '__main__':
    HOST = '0.0.0.0' 
    PORT = 8000
    
    # Threads diatur ke 16 sesuai spek i7-10700 Anda
    THREADS = 16

    print(f"==============================================")
    print(f"      SERVER AVARO (WAITRESS) RUNNING         ")
    print(f"==============================================")
    print(f" URL Lokal   : http://localhost:{PORT}")
    print(f" URL Jaringan: http://[IP-KOMPUTER]:{PORT}")
    print(f" Status      : DEBUG = False (Production Mode)")
    print(f" Threads     : {THREADS}")
    print(f"==============================================")

    serve(application, host=HOST, port=PORT, threads=THREADS)