# README — Tahapan Pengerjaan Proyek UTS

## 1. Inisialisasi Docker
    
Pertama membuat file `requirement.txt` pada directory `code/` yang berisikan package yang dibutuhkan:
```
django  
psycopg2-binary  
Pillow  
django-silk
```
Setelah itu membuat file `Dockerfile` untuk menginstal package pada file `requirement.txt`:
```
FROM python:3.12
ENV PYTHONBUFFERED=1  
WORKDIR /code  
COPY code/requirements.txt /code/  
RUN pip install -r requirements.txt
```
Kemudian membuat file `docker-compse.yml`:
    
```bash
services:  
 django:  
 container_name: simple_im  
 build: .  
 #command: sleep infinity  
 command: python manage.py runserver 0.0.0.0:8000  
 volumes:  
   - ./code:/code  
 ports:  
   - "8001:8000"  
postgres:  
 container_name: simple_db  
 image: postgres:latest  
 environment:  
   POSTGRES_DB: simple_im  
   POSTGRES_USER: simple_user  
   POSTGRES_PASSWORD: simple_password  
   PGDATA: /var/lib/postgresql/data/pgdata  
 ports:  
   - "5532:5432"  
 volumes:  
   - ./postgres-data:/var/lib/postgresql/data/pgdata
```
jika sudah maka jalankan perintah `docker compose up -d --build` pada terminal
    

----------

## 2. Inisialisasi Django

Proyek ini dibuat menggunakan framework **Django**,
Langkah selanjutnya yang dilakukan adalah menginisialisasi project Django dan membuat aplikasi utama:
```
django-admin startproject simpleim
python manage.py startapp core
```
Aplikasi `core` bertanggung jawab mengelola seluruh logika backend seperti database, view, dan URL.


----------

## 3. Konfigurasi Awal

-   Menambahkan `'core'` ke dalam `INSTALLED_APPS` di `simpleim/settings.py`.
-   Menyiapkan konfigurasi database menggunakan SQLite (default Django).
-   Membuat struktur folder `templates/core` untuk menyimpan file HTML.


----------

## 3. Membuat Model

Di dalam `core/models.py`, dibuat 4 model:
-   **Admin**: Untuk administrator.
-   **Supplier**: Untuk data pemasok barang.
-   **Category**: Untuk data kategori barang.
-   **Item**: Untuk data barang.
    

Setiap model memiliki field `created_at` dan `updated_at` yang otomatis terisi menggunakan:
``` python
created_at = models.DateTimeField(auto_now_add=True)
updated_at = models.DateTimeField(auto_now=True)
```
Relasi antar tabel menggunakan **ForeignKey**.  
Contoh:
``` python
category = models.ForeignKey(Category, on_delete=models.CASCADE)
```

---

## 4. Membuat Migrasi dan Migrate Database

Setelah model dibuat, selanjutnya melakukan migrasi database:
```
python manage.py makemigrations
python manage.py migrate
```
Proses ini akan menghasilkan tabel-tabel di database yang sesuai dengan model yang dibuat.

---

## 5. Membuat View dan URL Routing

Membuat view untuk melakukan operasi **Create dan Read** data:

-   **CreateView**: Menyediakan form untuk membuat data baru.
    
-   **ListView**: Menampilkan daftar data.
    

Menggunakan Class-Based Views (CBV) di `core/views.py`.

Setiap view dihubungkan melalui file `core/urls.py`, lalu `core/urls.py` di-include ke `simpleim/urls.py`.

Contoh URL routing:
``` py
path('items/create/', ItemCreateView.as_view(), name='item-create'),
path('items/', ItemListView.as_view(), name='item-list'),
```

---

## 6. Membuat Template HTML (Templates)

Template dibuat di folder `templates/core/`.  
File HTML yang dibuat antara lain:

-   `form.html`: untuk form input data.
    
-   `item_list.html`: untuk daftar barang.
    
-   `supplier_list.html`: untuk daftar supplier.
    

Template sederhana menggunakan `{{ form.as_p }}` untuk generate form otomatis dari Django.

---

## 7. Testing Aplikasi

-   Melakukan testing URL di browser untuk halaman HTML.

---
# ✅ Proyek Selesai
