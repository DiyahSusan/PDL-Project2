# Eksplorasi Database NoSQL
## Benchmark Database E-Commerce

Proyek ini membandingkan PostgreSQL, ScyllaDB, dan MongoDB menggunakan data e-commerce.

## Persiapan

Jalankan docker dengan menjalankan command berikut pada root directory.
```
docker-compose up
```

Pasang Python 3.10+ dan dependency yang digunakan:

```bash
pip install cassandra-driver Faker "psycopg[binary]" pymongo
```

Terapkan skema dari `ScyllaDB/schema.cql` dan `RDBMS/schema_postgres.sql` ke database masing-masing. Skema ScyllaDB dan PostgreSQL menghapus struktur lama sebelum membuat ulang tabel.

## Menjalankan Program

Dari folder utama proyek:

```bash
python ScyllaDB/seed_scylla.py
```

Untuk migrasi, sesuaikan koneksi PostgreSQL di `RDBMS/migrate_scylla_to_postgres.py`, lalu jalankan:

```bash
python RDBMS/migrate_scylla_to_postgres.py
python MongoDB/migrate_to_mongo.py
```

## Verifikasi

```
docker exec -it scylla_db cqlsh 
```
```
docker exec -it mongo_db mongosh
```
```
docker exec -it postgres_db psql -U postgres -d ecommerce
```
Jalankan query yang sesuai pada database yang ingin diperiksa.
