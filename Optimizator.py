from Queue import Queue, Cell

class Optimizator():
    def __init__(self, file_name):
        self.__buff = Queue()
        self.__load_buf()
        self.__adress = file_name
        self.__max_quantity = 50
        self.__movements = self.__movement_check()
        

    def get(self, id, quantity):
        """Берем из ячейки <id> количество <quantity>"""
        text = self.__load_stock_data()
        for i in range(0, len(text), 2):
            if str(text[i]) == id:
                ###Логику дописать
                text[i + 1] = text[i + 1] - quantity
                self.__add_in_buf(Cell(str(text[i]), text[i + 1]))
                print(self.__buff.get_elems())
                self.__save_stock_data(text)
                break
        self.__movements = self.__movement_check()
        return

    def __load_stock_data(self):
        """База в виде файла"""
        with open(self.__adress, "r", encoding="UTF-8") as file:
            text = list(map(int, file.read().split()))
        return text

    def __save_stock_data(self, text):
        """Сохраняем изменения"""
        with open(self.__adress, "w", encoding="UTF-8") as file:
            for i in text:
                print(i, file = file)

    def __load_buf(self):
        """Подгружаем буфер"""
        with open("buf.txt", "r", encoding="UTF-8") as file:
            text = list(map(int, file.read().split()))
        for i in range(0, len(text), 2):
            self.__add_in_buf(Cell(str(text[i]), text[i+1]))

    def __save_buf(self):
        """Сохраняем буфер"""
        text = self.__buff.get_elems()
        with open("buf.txt", "w", encoding="UTF-8") as file:
            for i in text:
                print(f'{i[0]} \n{i[1]}', file = file)

    def __add_in_buf(self, cell):
        """Пушим в буфер ячейку с измененным количеством содержимого"""
        self.__buff.push(cell)
        self.__save_buf()

    def get_buf(self):
        """Смотрим какие ячейки с измененным содержимым"""
        return self.__buff.get_elems()

    def get_movements(self):
        """ВЫнимаем возможные перемещения"""
        if self.__movements != None:
            return self.__movements
        else:
            return []
    
    def __movement_check(self):
        """Поиск возможных перемещений"""
        que = self.__buff.get_elems()
        movements = []
        for i in que:
            if i[1] > self.__max_quantity / 2:
                break
            for j in que:
                if i[0] != j[0]:
                    if j[1] + i[1] > self.__max_quantity:
                        break
                    else:
                        movement = []
                        movement.append(i[0])
                        movement.append(j[0])
                        movements.append(movement)
        if len(movements) != 0:
            return movements
        else: 
            return None

    def movement(self, id1, id2):
        """Перемещение из ячейки <id2> в <id1>"""
        ind1 = None
        ind2 = None
        text = self.__load_stock_data()
        for i in range(len(text)):
            if str(text[i]) == id1:
                ind1 = i
            if str(text[i]) == id2:
                ind2 = i
        if ind1 == None or ind2 == None:
            return
        else:
            text[ind1 + 1], text[ind2 + 1] = text[ind1 + 1] + text[ind2 + 1], 0
            self.__save_stock_data(text)
            self.__buff.pop(id1)
            self.__buff.pop(id2)
            self.__save_buf()
            self.__movements = self.__movement_check()