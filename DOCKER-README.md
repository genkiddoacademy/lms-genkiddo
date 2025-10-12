# Docker Deployment untuk Frappe LMS

Dokumentasi ini menjelaskan cara menjalankan aplikasi Frappe LMS menggunakan Docker.

## 🚀 Quick Start

### Metode 1: Menggunakan Script Otomatis (Recommended)

```bash
# Jalankan script build dan run
./build-and-run.sh
```

### Metode 2: Manual Build dan Run

```bash
# 1. Build Docker image
docker build -t lms-genkiddo:latest .

# 2. Start semua services
docker-compose -f docker-compose.standalone.yml up -d

# 3. Monitor logs (optional)
docker-compose -f docker-compose.standalone.yml logs -f lms-app
```

## 📋 Informasi Akses

Setelah container berjalan, Anda dapat mengakses:

-   **LMS Application**: http://localhost:8000
-   **Socket.IO Server**: http://localhost:9000
-   **MariaDB**: localhost:3306
-   **Redis**: localhost:6379

## 🔑 Kredensial Default

-   **Username**: Administrator
-   **Password**: admin

## 📦 Arsitektur Docker

### Services yang Dijalankan:

1. **lms-app**: Aplikasi utama Frappe LMS
2. **mariadb**: Database MySQL/MariaDB
3. **redis**: Cache server untuk session dan queue

### Volumes:

-   `mariadb-data`: Persistent storage untuk database
-   `redis-data`: Persistent storage untuk Redis
-   `./sites`: Mount local sites directory (optional)

## 🛠️ Perintah Berguna

```bash
# Melihat status containers
docker-compose -f docker-compose.standalone.yml ps

# Melihat logs aplikasi
docker-compose -f docker-compose.standalone.yml logs -f lms-app

# Restart aplikasi
docker-compose -f docker-compose.standalone.yml restart lms-app

# Stop semua services
docker-compose -f docker-compose.standalone.yml down

# Stop dan hapus volumes (HATI-HATI: akan menghapus data)
docker-compose -f docker-compose.standalone.yml down -v

# Rebuild aplikasi
docker-compose -f docker-compose.standalone.yml up --build
```

## 🔧 Development Mode

Untuk development, Anda bisa mount source code:

```yaml
# Tambahkan ke docker-compose.standalone.yml di service lms-app
volumes:
    - ./lms:/home/frappe/frappe-bench/apps/lms
    - ./sites:/home/frappe/frappe-bench/sites
```

## 🐛 Troubleshooting

### Aplikasi tidak bisa diakses

1. Pastikan semua containers berjalan: `docker ps`
2. Cek logs aplikasi: `docker-compose logs lms-app`
3. Tunggu 2-3 menit untuk inisialisasi lengkap

### Database connection error

1. Pastikan MariaDB container berjalan
2. Cek logs MariaDB: `docker-compose logs mariadb`
3. Reset containers: `docker-compose down && docker-compose up`

### Port sudah digunakan

Jika port 8000/9000 sudah digunakan, edit `docker-compose.standalone.yml`:

```yaml
ports:
    - "8080:8000" # Ganti 8000 ke 8080
    - "9090:9000" # Ganti 9000 ke 9090
```

## 📝 Catatan Penting

1. **First Run**: Proses pertama kali akan membutuhkan 3-5 menit untuk setup database dan install aplikasi
2. **Data Persistence**: Data database dan Redis akan tersimpan di Docker volumes
3. **Resource Usage**: Aplikasi membutuhkan minimal 2GB RAM untuk berjalan dengan lancar
4. **Network**: Semua services menggunakan custom network `lms-network`

## 🔄 Update Aplikasi

Untuk update aplikasi ke versi terbaru:

```bash
# Pull latest code
git pull origin main

# Rebuild dan restart
docker-compose -f docker-compose.standalone.yml up --build
```

## 📞 Support

Jika mengalami masalah, silakan:

1. Cek logs menggunakan perintah di atas
2. Buat issue di repository GitHub
3. Sertakan output logs dan konfigurasi sistem
