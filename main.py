from Queue import Queue, Cell
from Optimizator import Optimizator

stock = {'1': 50, '2': 50, '3': 30, '4': 20, '5': 50, '6': 60, '7': 50, '8': 10, '9': 20}

q = Queue()
for i in stock.keys():
    q.push(Cell(i, stock[i]))

#print(q.get_elems())

q.push(Cell('1', 20))
#print(q.get_elems())
q.push(Cell('5', 5))
#print(q.get_elems())

opti = Optimizator("Stock.txt");
opti.get('1', 0);
print(opti.get_buf())