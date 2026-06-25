# Music-Recommendation

# Alia - Neo4j
# Music Recommendation - Neo4j Database Setup

Panduan ini digunakan untuk menyiapkan database Neo4j yang digunakan pada project Music Recommendation.

---

## Prasyarat

Pastikan sudah menginstall:

- Python 3.10+
- Neo4j Desktop
- Library Neo4j Python Driver

Install library:

```bash
pip install neo4j
```

---

## Struktur Folder

Pastikan struktur project seperti berikut:

```text
Music-Recommendation
│
├── neo4j
│   ├── data
│   │   ├── music_clean.csv
│   │   └── history_clean.csv
│   │
│   ├── import_data.py
│   ├── load_database.py
│   ├── queries.py
│   └── test_query.py
│
└── README.md
```

---

## Langkah 1 - Membuat Database Neo4j

1. Buka Neo4j Desktop.
2. Klik **Create Instance**.
3. Beri nama database:

```
musikdb
```

4. Buat password.
5. Klik **Start** sampai status menjadi:

```
Running
```

---

## Langkah 2 - Membuka Folder Import Neo4j

1. Pada Neo4j Desktop, buka instance `musikdb`.
2. Klik menu **Open Folder**.
3. Pilih folder:

```
Import
```

Akan terbuka folder import Neo4j.

---

## Langkah 3 - Copy Dataset

Dari project ini:

```text
neo4j/data/music_clean.csv
neo4j/data/history_clean.csv
```

Copy kedua file tersebut ke folder import Neo4j yang dibuka pada langkah sebelumnya.

Hasilnya:

```text
Import
│
├── music_clean.csv
└── history_clean.csv
```

---

## Langkah 4 - Konfigurasi Koneksi

Buka file:

```text
neo4j/import_data.py
```

Ubah bagian berikut sesuai password Neo4j yang dibuat:

```python
URI = "bolt://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "PASSWORD_NEO4J_ANDA"
```

Contoh:

```python
PASSWORD = "12345678"
```

---

## Langkah 5 - Import Data ke Neo4j

Buka terminal pada root project.

Jalankan:

```bash
python neo4j/load_database.py
```

Proses ini akan:

- Membuat node Song
- Membuat node User
- Membuat relasi LISTENED
- Mengimpor seluruh dataset ke Neo4j

Tunggu hingga proses selesai.

Output yang diharapkan:

```text
=== Import Songs ===
Song imported!

=== Import History ===
History imported!

=== DATABASE RESULT ===

[{'songs': 7794}]
[{'users': 23795}]
[{'relations': 1575399}]
```

---

## Langkah 6 - Verifikasi Database

Jalankan:

```bash
python neo4j/test_query.py
```

Output yang diharapkan:

```text
=== ALL SONGS ===
...

=== USER HISTORY ===
...

=== RELATION ===
...
```

Jika output muncul, maka koneksi Python ↔ Neo4j berhasil.

---

## Struktur Database

### Node

#### Song

```text
(:Song)
```

Contoh properti:

```text
track_id
name
artist
genre
year
```

#### User

```text
(:User)
```

Contoh properti:

```text
user_id
```

---

### Relationship

```text
(:User)-[:LISTENED]->(:Song)
```

Properti:

```text
playcount
```

---

## Query yang Tersedia

File:

```text
neo4j/queries.py
```

Berisi query:

- GET_ALL_SONGS
- GET_ALL_USERS
- GET_USER_HISTORY
- GET_USER_SONG_RELATION
- GET_SONG_BY_GENRE

---

## Troubleshooting

### Authentication Failure

Error:

```text
AuthError: The client is unauthorized due to authentication failure
```

Solusi:

- Periksa password pada `import_data.py`
- Pastikan Neo4j dalam kondisi Running

---

### CSV Not Found

Error:

```text
Couldn't load the external resource
```

Solusi:

Pastikan:

```text
music_clean.csv
history_clean.csv
```

sudah berada di folder Import Neo4j.

---

### Database Tidak Running

Pastikan status database pada Neo4j Desktop adalah:

```text
Running
```

sebelum menjalankan script Python.