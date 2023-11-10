from Stock import Stock
import sqlite3 as sql

stock = Stock()
#stock.add('0005', 10, '1')
stock.movement()

#db = sql.connect('stock.db')
#cur = db.cursor()
#cur.execute("UPDATE stock SET quantity = ? WHERE id = ?", (30, '0001'))
#db.commit()