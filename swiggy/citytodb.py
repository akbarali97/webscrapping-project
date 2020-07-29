
import sqlite3

with open("swiggycitylist-kerala.txt") as f:
    read = f.readlines()
    for row in read:
        row = row.strip()
        print(row)
        with sqlite3.connect("swiggy_db.sqlite3") as con:
            con.execute("INSERT INTO avail_cities_kerala (city) VALUES(?);",[row])


