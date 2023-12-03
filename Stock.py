import sqlite3 as sql
from statistics import quantiles
from Optimizator import Optimizator
from Cell import Cell
import pandas as pd

class Stock():
    def __init__(self, db_adress):
        self.__db_adress = db_adress
        self.__db_type, self.__db_params, self.__db = self.__init_stock(self.__db_adress)
        self.__optimizator = self.__init_optimizator()
        self.__commit()

    def __commit(self):
        if self.__db_type == 'db':
            self.__db.commit()
        elif self.__db_type == 'txt':
            f = open(self.__db_adress, 'w')
            for i in self.__db_params:
                f.write(str(i) + ' ')
            f.write('\n')
            for i in self.__db:
                f.write(str(i[0]) + ' ')
                f.write(str(i[1]) + ' ')
                f.write(str(i[2]))
                f.write('\n')
            f.close()
        else:
            ids, quantities, types = [], [], []
            for i in self.__db:
                ids.append(i[0])
                quantities.append(i[1])
                types.append(i[2])
            df1 = pd.DataFrame({'id':ids, 'quantity': quantities, 'type': types})
            df2 = pd.DataFrame({'i': [self.__db_params[0]], 'j': [self.__db_params[1]], 'k': [self.__db_params[2]], 'size': [self.__db_params[3]]})
            writer = pd.ExcelWriter('stock.xlsx')
            df1.to_excel(writer, 'stock')
            df2.to_excel(writer, 'params') 
            writer.save()



    def add(self, cid, cquantity, ctype):
        """Метод добавляющий что-то в ячейку и возвращает обновленные данные о ней"""
        if self.__db_type == 'db':
            cursor = self.__db.cursor()
            if cursor.execute("SELECT quantity FROM stock WHERE id=?", (cid,)).fetchone()[0] == 0 and cquantity <= self.__db_params[3] and cquantity > 0:
                cursor.execute("UPDATE stock SET quantity=? WHERE id=?", (cquantity, cid))
                cursor.execute("UPDATE stock SET type=? WHERE id=?", (ctype, cid))
                self.__db.commit()
                if cquantity < self.__db_params[3]:
                    self.__optimizator.add(Cell(cid, cquantity, ctype))
                return (cid, cquantity, ctype)
            else:
                return ()
        else:
            for i in range(len(self.__db)):
                if self.__db[i][0] == cid:
                    if self.__db[i][1] == 0 and cquantity <= self.__db_params[3] and cquantity > 0:
                        self.__db[i][1] = cquantity
                        self.__db[i][2] = ctype
                        if cquantity < self.__db_params[3]:
                            self.__optimizator.add(Cell(cid, cquantity, ctype))
                        self.__commit()
                        return (cid, cquantity, ctype)
                    else:
                        return ()

    def get(self, cid, cquantity):
        """Метод для извлечения из ячейким чего-либо и возвращает обновленные данные о ячейке"""
        if self.__db_type == 'db':
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
                if old_quant < self.__db_params[3]:
                    ctype = cursor.execute("SELECT type FROM stock WHERE id=?", (cid,)).fetchone()[0]
                    self.__optimizator.erase(Cell(cid, old_quant, ctype))
                cursor.execute("UPDATE stock SET quantity=? WHERE id=?", (0, cid))
                cursor.execute("UPDATE stock SET type=? WHERE id=?", ("None", cid))
                self.__db.commit()
                return (cid, 0, "None")
            else:
                return ()
        else:
            old_quant = None
            cell_index = None
            for i in range(len(self.__db)):
                if self.__db[i][0] == cid:
                    old_quant = self.__db[i][1]
                    cell_index = i
                    break
            if  old_quant > cquantity:
                old_quant -= cquantity
                self.__db[cell_index][1] = old_quant
                self.__optimizator.add(Cell(cid, old_quant, self.__db[cell_index][2]))
                self.__commit()
                return (cid, old_quant, self.__db[cell_index][2])
            elif old_quant == cquantity:
                if old_quant < self.__db_params[3]:
                    self.__optimizator.erase(Cell(cid, old_quant, self.__db[cell_index][2]))
                self.__db[cell_index][1] = 0
                self.__db[cell_index][2] = "None"
                self.__commit()
                return (cid, 0, "None")
            else:
                return ()

    def movement(self):
        """Метод для выполнения перемещений по складу"""
        clusters = self.__optimizator.divide_into_clusters()
        self.__optimizator.swap(clusters)
        self.__commit()

    def get_db(self):
        """Метод для вывода данных БД"""
        if self.__db_type == 'db':
            cursor = self.__db.cursor()
            return cursor.execute("SELECT * FROM stock").fetchall()
        else:
            return self.__db

    def get_cell_quantity(self, cid):
        """Метод для получения из БД заполненость ячейки cid"""
        if self.__db_type == 'db':
            cursor = self.__db.cursor()
            return cursor.execute("SELECT quantity FROM stock WHERE id=?", (cid,)).fetchone()[0]
        else:
            for i in range(len(self.__db)):
                if self.__db[i][0] == cid:
                    return self.__db[i][1]

    def get_cell_type(self, cid):
        """Метод для получения из БД тип содержимого ячейки cid"""
        if self.__db_type == 'db':
            cursor = self.__db.cursor()
            return cursor.execute("SELECT type FROM stock WHERE id=?", (cid,)).fetchone()[0]
        else:
            for i in range(len(self.__db)):
                if self.__db[i][0] == cid:
                    return self.__db[i][2]

    def __init_optimizator(self):
        optimizator = Optimizator(self.__db_type, self.__db_params, self.__db)
        cells = []
        if self.__db_type == 'db':
            cursor = self.__db.cursor()
            cells = cursor.execute("SELECT * FROM stock").fetchall()
        else:
            cells = self.__db
        for i in cells:
            if i[1] < self.__db_params[3] and i[1] > 0:
                optimizator.add(Cell(i[0], i[1], i[2]))
        return optimizator

    def __load_txt_db(self, db_adress):
        cells = []
        result = []
        params = []
        with open(db_adress, 'r', encoding="UTF-8") as file_in:
             cells = list(map(str, file_in.read().split()))
        for i in range(4, len(cells) - 1, 3):
            result.append([cells[i], int(cells[i + 1]), cells[i + 2]])
        params = cells[:4]
        params[0], params[1], params[2], params[3] = int(params[0]), int(params[1]), int(params[2]), int(params[3])
        return params, result

    def __load_xlsx_db(self, db_adress):
        result = []
        x = pd.ExcelFile(db_adress)
        df = x.parse('params')
        params = [int(df.iloc[0]['i']), int(df.iloc[0]['j']), int(df.iloc[0]['k']), int(df.iloc[0]['size'])]
        x = pd.ExcelFile(db_adress)
        df = x.parse('stock')
        for i in range(params[0]*params[1]*params[2]):
            cell_id = str(df.iloc[i]['id'])
            while len(cell_id) < 4:
                cell_id = '0' + cell_id
            result.append([cell_id, int(df.iloc[i]['quantity']), df.iloc[i]['type']])
        return params, result


    def __init_stock(self, db_adress):
        if db_adress[len(db_adress)-2:] == 'db': 
            con = sql.connect("stock.db")
            cursor = con.cursor()
            params = cursor.execute("SELECT * FROM params").fetchall()
            return 'db', params, con
        elif db_adress[len(db_adress)-3:] == 'txt':
            params, db = self.__load_txt_db(db_adress)
            return 'txt', params, db
        elif db_adress[len(db_adress)-4:] == 'xlsx':
            params, db = self.__load_xlsx_db(db_adress)
            return 'xlsx', params, db

if __name__ == '__main__':
    stock = Stock('stock.xlsx')