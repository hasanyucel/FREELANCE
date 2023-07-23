import sqlite3
import json

# JSON dosyasının adı
json_dosya_adi = "sureler.json"

# Veritabanı dosyasının adı
db_dosya_adi = "kuran_database.db"

# Veritabanı bağlantısı oluşturma
baglanti = sqlite3.connect(db_dosya_adi)
cursor = baglanti.cursor()

# Tabloyu oluşturma (eğer daha önce oluşturulmamışsa)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS sureler (
        sure_no INTEGER PRIMARY KEY,
        ayet_sayisi INTEGER,
        sure_adi TEXT
    )
''')

# JSON dosyasından verileri okuma ve veritabanına eklenmesi
with open(json_dosya_adi, 'r', encoding='utf-8') as dosya:
    sureler = json.load(dosya)
    for sure in sureler['sureler']:
        sure_no = sure['sure_numarasi']
        ayet_sayisi = sure['ayet_sayisi']
        sure_adi = sure['sure_adi']
        cursor.execute('INSERT INTO sureler (sure_no, ayet_sayisi, sure_adi) VALUES (?, ?, ?)', (sure_no, ayet_sayisi, sure_adi))

# Değişiklikleri kaydet ve bağlantıyı kapat
baglanti.commit()
baglanti.close()

print("Veriler başarıyla SQLite veritabanına aktarıldı.")
