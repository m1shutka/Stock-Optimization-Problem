import sqlite3 as sql
from Optimizator import Optimizator
from Cell import Cell

class Stock():
    def __init__(self):
        self.__db = sql.connect("stock.db")
        self.__max_quantity = 50
        self.__optimizator = self.__init_optimizator("stock.db")

    def add(self, cid, cquantity, ctype):
        """Метод добавляющий что-то в ячейку и возвращает обновленные данные о ней"""
        cursor = self.__db.cursor()
        if cursor.execute("SELECT quantity FROM stock WHERE id=?", (cid,)).fetchone()[0] == 0 and cquantity <= self.__max_quantity and cquantity > 0:
            cursor.execute("UPDATE stock SET quantity=? WHERE id=?", (cquantity, cid))
            cursor.execute("UPDATE stock SET type=? WHERE id=?", (ctype, cid))
            self.__db.commit()
            if cquantity < 50:
                self.__optimizator.add(Cell(cid, cquantity, ctype))
            return (cid, cquantity, ctype)
        else:
            return ()

    def get(self, cid, cquantity):
        """Метод для извлечения из ячейким чего-либо и возвращает обновленные данные о ячейке"""
        cursor = self.__db.cursor()
        old_quant = cursor.execute("SELECT quantity FROM stock WHERE id=?", (cid,)).fetchone()[0]
        if  old_quant > cquantity:
            old_quant -= cquantity
            cursor.execute("UPDATE stock SET quantity=? WHERE id=?", (old_quant, cid))
            self.__db.commit()
            ctype = cursor.execute("SELECT type FROM stock WHERE id=?", (cid,)).fetchone()[0]
            self.__optimizator.add(Cell(cid, old_quant, ctype))
            return (cid, old_quant, ctype)
        elif old_quant == cquantity:
            if old_quant < 50:
                ctype = cursor.execute("SELECT type FROM stock WHERE id=?", (cid,)).fetchone()[0]
                self.__optimizator.erase(Cell(cid, old_quant, ctype))
            cursor.execute("UPDATE stock SET quantity=? WHERE id=?", (0, cid))
            cursor.execute("UPDATE stock SET type=? WHERE id=?", ("None", cid))
            self.__db.commit()
            return (cid, 0, "None")
        else:
            return ()

    def movement(self):
        """Метод для выполнения перемещений по складу"""
        clusters = self.__optimizator.divide_into_clusters()
        self.__optimizator.swap(clusters)

    def get_db(self):
        """Метод для вывода данных БД"""
        cursor = self.__db.cursor()
        return cursor.execute("SELECT * FROM stock").fetchall()

    def get_cell_quantity(self, cid):
         cursor = self.__db.cursor()
         return cursor.execute("SELECT quantity FROM stock WHERE id=?", (cid,)).fetchone()[0]

    def get_cell_type(self, cid):
         cursor = self.__db.cursor()
         return cursor.execute("SELECT type FROM stock WHERE id=?", (cid,)).fetchone()[0]

    def __init_optimizator(self, db_adress):
        optimizator = Optimizator(db_adress, self.__max_quantity)
        cursor = self.__db.cursor()
        cells = cursor.execute("SELECT * FROM stock").fetchall()
        for i in cells:
            if i[1] < self.__max_quantity and i[1] > 0:
                optimizator.add(Cell(i[0], i[1], i[2]))
        return optimizator