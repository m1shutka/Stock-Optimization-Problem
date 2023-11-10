class Cell():
    def __init__(self, cid, cquantity, ctype = None):
        """Класс ячейка"""
        self.__id = cid
        self.__quantity = cquantity
        self.__type = ctype

    def get_id(self):
        return self.__id

    def get_quantity(self):
        return self.__quantity

    def get_type(self):
        return self.__type