import xml.etree.ElementTree as ET
import sqlite3

xml_file = "kuranikerim.xml"
db_file = "kuran_database.db"

def create_table(table_name):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    create_table_sql = f'''
    CREATE TABLE IF NOT EXISTS "{table_name}" (
        "index" TEXT,
        "sura" TEXT,
        "aya" TEXT,
        "text" TEXT,
        PRIMARY KEY("index")
    );
    '''
    cursor.execute(create_table_sql)
    conn.commit()
    conn.close()

def insert_data_to_db(xml_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    tree = ET.parse(xml_file)
    root = tree.getroot()

    for table in root.findall('.//table'):
        table_name = table.get('name')
        index = ""
        sura = ""
        aya = ""
        text = ""

        for column_data in table.findall('.//column'):
            column_name = column_data.get('name')

            if column_name == 'index':
                index = column_data.text
            if column_name == 'sura':
                sura = column_data.text
            if column_name == 'aya':
                aya = column_data.text
            if column_name == 'text':
                text = column_data.text
        cursor.execute(f'INSERT OR REPLACE INTO "{table_name}" ("index", "sura", "aya", "text") VALUES (?, ?, ?, ?)', (index, sura, aya, text))

    conn.commit()
    conn.close()


tables = ["de_aburida","en_yusufali","fr_hamidullah","it_piccardo","ja_japanese","ku_asan","quran_text","ru_muntahab","tr_diyanet","uz_sodik"]

for table in tables:
    create_table(table)
insert_data_to_db(xml_file)



