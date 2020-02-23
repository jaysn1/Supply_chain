import csv, os, sqlite3

def insert_data():
    con = sqlite3.connect('site.db')
    cur = con.cursor()
    with open(os.getcwd() + '/flasksite/data/sales_data.csv','r',encoding='utf-8-sig') as f:
        dr = csv.DictReader(f)
        to_db = [(i['item'],i['store'],i['date'],i['sales']) for i in dr]

    #print(to_db)
    cur.executemany("INSERT INTO sales (product_id, store_id, purchase_date, sale_sum) VALUES (?, ?, ?, ?);", to_db)
    con.commit()
    con.close()