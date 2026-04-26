# 1. Gunakan versi Python yang ringan (Sesuaikan versinya jika Anda pakai 3.11 atau 3.12)
FROM python:3.10-slim

# 2. Atur variabel environment agar Python berjalan lebih stabil di dalam container
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# TAMBAHAN: Install dan aktifkan locale id_ID.UTF-8 untuk format tanggal/waktu Indonesia
RUN apt-get update && apt-get install -y locales \
    && sed -i -e 's/# id_ID.UTF-8 UTF-8/id_ID.UTF-8 UTF-8/' /etc/locale.gen \
    && dpkg-reconfigure --frontend=noninteractive locales \
    && rm -rf /var/lib/apt/lists/*

ENV LANG=id_ID.UTF-8
ENV LC_ALL=id_ID.UTF-8

# 3. Tentukan folder kerja di dalam container
WORKDIR /app

# 4. Salin file daftar library ke dalam container
COPY requirements.txt /app/

# 5. Install semua library yang dibutuhkan (termasuk Django dan Waitress)
RUN pip install --no-cache-dir -r requirements.txt

# 6. Salin semua file proyek Anda ke dalam container
COPY . /app/

# 7. Kumpulkan file statis (CSS/JS) milik Django dan Bootstrap
RUN python manage.py collectstatic --noinput

# 8. Buka port 8080 untuk jalur komunikasi
EXPOSE 8000

# 9. Eksekusi Migrasi lalu Nyalakan Waitress
# PENTING: Jika folder wsgi Anda bernama 'avaro', ganti 'nama_project' menjadi 'avaro'
CMD sh -c "python manage.py makemigrations && python manage.py migrate && waitress-serve --listen=0.0.0.0:8000 avaro.wsgi:application"