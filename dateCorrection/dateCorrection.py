import sqlite3,sys,os.path

def correctDates(db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute('update StockPrice set date = substr(date, 7) || "/" || substr(date,4,2)   || "/" || substr(date, 1,2) where date like "__/__/____"')
    conn.commit()
    conn.close()

def check_quit(inp):
    if inp == 'q':
        sys.exit(0)

db_exists = os.path.exists('tilemountain.sqlite')
if db_exists:
    correctDates('tilemountain.sqlite')
    print("Tilemountain has been updated.")

db_exists = os.path.exists('wallsandfloors.sqlite')
if db_exists:
    correctDates('wallsandfloors.sqlite')
    print("Wallsandfloors has been updated.")

x = str(input("Please press 'q' to exit: "))
check_quit(x)