from Queue import Queue
from Cell import Cell
import sqlite3 as sql

class Optimizator():
    def __init__(self, db_adress, max_quantity):
        self.__buff = {}
        self.__max_quantity = max_quantity
        #self.__movements = []
        self.__db_adress = db_adress

    def add(self, cell):
        """Добавляем изменения"""
        if cell.get_type() in self.__buff.keys():
            self.__buff[cell.get_type()].push(cell)
        else:
            self.__buff[cell.get_type()] = Queue()
            self.__buff[cell.get_type()].push(cell)

    def erase(self, cell):
        if cell.get_type() in self.__buff.keys():
             self.__buff[cell.get_type()].pop(cell.get_id())

    def __max_cluster(self, changes):
        """Формирование кластера"""
        print("Зашел в max_cluster")
        result = []
        quantity = 0
        for i in changes:
            if len(result) == 0:
                result.append(i)
                quantity += i[1]
            else:
                if quantity + i[1] <= self.__max_quantity:
                    result.append(i)
                    quantity += i[1]
        print("Ввышел из max_cluster")
        return result

    def divide_into_clusters(self):
        """Разделение на множества"""
        print("Зашел в divide_into_clusters")
        result = {}
        for i in self.__buff.keys():
            changes = self.__buff[i].get_elems()
            clusters = []
            while len(changes) > 0:
                cluster = self.__max_cluster(changes)
                clusters.append(cluster)
                for j in cluster:
                    indx = self.__find_indx(changes, j)
                    if indx != None:
                        changes.pop(indx)
            result[i] = clusters
        print("Ввышел из divide_into_clusters")
        return result
   
    def swap(self, clusters):
        """Сжатие множеств"""
        print("Зашел в swap")
        db = sql.connect(self.__db_adress)
        cursor = db.cursor()
        for ctype in clusters.keys():
            for cluster in clusters[ctype]:
                if len(cluster) > 1:
                    new_quant = cluster[0][1]
                    for i in range(1, len(cluster)):
                        new_quant += cluster[i][1]
                        cursor.execute("UPDATE stock SET quantity = ? WHERE id = ?", (0, cluster[i][0]))
                        cursor.execute("UPDATE stock SET type = ? WHERE id = ?", ('None', cluster[i][0]))
                        db.commit()
                        self.__buff[ctype].pop(cluster[i][0])
                    cursor.execute("UPDATE stock SET quantity = ? WHERE id = ?", (new_quant, cluster[0][0]))
                    db.commit()
                    if new_quant < self.__max_quantity:
                        self.__buff[ctype].pop(cluster[0][0])
                        self.__buff[ctype].push(Cell(cluster[0][0], new_quant, ctype))
                    else:
                        self.__buff[ctype].pop(cluster[0][0])
        print("Ввышел из swap")

    def __find_indx(self, changes, claster):
        print("Зашел в find_indx")
        for i in range(len(changes)):
            if changes[i] == claster:
                return i
        print("Ввышел из find_indx")
        return None