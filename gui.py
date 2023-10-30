from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showerror, showinfo
from Optimizator import Optimizator

def btn_click1():
    quantity = entry.get()
    optimizator.get('1', int(quantity))
    set_buttons()
    set_labels()

def btn_click2():
    quantity = entry.get()
    optimizator.get('2', int(quantity))
    set_buttons()
    set_labels()

def btn_click3():
    quantity = entry.get()
    optimizator.get('3', int(quantity))
    set_buttons()
    set_labels()

def btn_click4():
    quantity = entry.get()
    optimizator.get('4', int(quantity))
    set_buttons()
    set_labels()

def btn_click5():
    quantity = entry.get()
    optimizator.get('5', int(quantity))
    set_buttons()
    set_labels()

def btn_click6():
    quantity = entry.get()
    optimizator.get('6', int(quantity))
    set_buttons()
    set_labels()

def btn_click7():
    quantity = entry.get()
    optimizator.get('7', int(quantity))
    set_buttons()
    set_labels()

def btn_click8():
    quantity = entry.get()
    optimizator.get('8', int(quantity))
    set_buttons()
    set_labels()

def btn_click9():
    quantity = entry.get()
    optimizator.get('9', int(quantity))
    set_buttons()
    set_labels()

def btn_click10():
    quantity = entry.get()
    optimizator.get('10', int(quantity))
    set_buttons()
    set_labels()

def btn_click11():
    quantity = entry.get()
    optimizator.get('11', int(quantity))
    set_buttons()
    set_labels()

def btn_click12():
    quantity = entry.get()
    optimizator.get('12', int(quantity))
    set_buttons()
    set_labels()

def btn_click13():
    quantity = entry.get()
    optimizator.get('13', int(quantity))
    set_buttons()
    set_labels()

def btn_click14():
    quantity = entry.get()
    optimizator.get('14', int(quantity))
    set_buttons()
    set_labels()

def btn_click15():
    quantity = entry.get()
    optimizator.get('15', int(quantity))
    set_buttons()
    set_labels()

def btn_mov_click():
    id1 = entry1.get()
    id2 = entry2.get()
    optimizator.movement(id1, id2)
    set_buttons()
    set_labels()

def load_stock_data():
        with open("Stock.txt", "r", encoding="UTF-8") as file:
            text = list(map(int, file.read().split()))
        return text

def set_buttons():
    text = load_stock_data()
    btn1['text'] = str(text[1])
    btn2['text'] = str(text[3])
    btn3['text'] = str(text[5])
    btn4['text'] = str(text[7])
    btn5['text'] = str(text[9])
    btn6['text'] = str(text[11])
    btn7['text'] = str(text[13])
    btn8['text'] = str(text[15])
    btn9['text'] = str(text[17])
    btn10['text'] = str(text[19])
    btn11['text'] = str(text[21])
    btn12['text'] = str(text[23])
    btn13['text'] = str(text[25])
    btn14['text'] = str(text[27])
    btn15['text'] = str(text[29])

def set_labels():
    movements = optimizator.get_movements()
    result = ''
    for i in movements:
        result += i[0] + '->' + i[1] + ', '
    label1['text'] = f'Возможные перестановки: {result}'

    buf = optimizator.get_buf()
    print(f'gui -{buf}')
    result = ''
    for i in buf:
        result += str(i[0]) + ': ' + str(i[1]) + ', '
    label2['text'] = f'Буфер: {result}'

if  __name__ == "__main__":
    optimizator = Optimizator("Stock.txt")
    root = Tk()     
    root.title("Склад")     
    root.geometry("460x330+740+270")    
    root.resizable(False, False)
   
    btn1 = ttk.Button(text="1", command=btn_click1)
    btn1.place(x=20, y=20, width = 60, height = 60)
    btn2 = ttk.Button(text="2", command=btn_click2)
    btn2.place(x=90, y=20, width = 60, height = 60)
    btn3 = ttk.Button(text="3", command=btn_click3)
    btn3.place(x=160, y=20, width = 60, height = 60)
    btn4 = ttk.Button(text="4", command=btn_click4)
    btn4.place(x=230, y=20, width = 60, height = 60)
    btn5 = ttk.Button(text="5", command=btn_click5)
    btn5.place(x=300, y=20, width = 60, height = 60)

    btn6 = ttk.Button(text="1", command=btn_click6)
    btn6.place(x=20, y=90, width = 60, height = 60)
    btn7 = ttk.Button(text="2", command=btn_click7)
    btn7.place(x=90, y=90, width = 60, height = 60)
    btn8 = ttk.Button(text="3", command=btn_click8)
    btn8.place(x=160, y=90, width = 60, height = 60)
    btn9 = ttk.Button(text="4", command=btn_click9)
    btn9.place(x=230, y=90, width = 60, height = 60)
    btn10 = ttk.Button(text="5", command=btn_click10)
    btn10.place(x=300, y=90, width = 60, height = 60)

    btn11 = ttk.Button(text="1", command=btn_click11)
    btn11.place(x=20, y=160, width = 60, height = 60)
    btn12 = ttk.Button(text="2", command=btn_click12)
    btn12.place(x=90, y=160, width = 60, height = 60)
    btn13 = ttk.Button(text="3", command=btn_click13)
    btn13.place(x=160, y=160, width = 60, height = 60)
    btn14 = ttk.Button(text="4", command=btn_click14)
    btn14.place(x=230, y=160, width = 60, height = 60)
    btn15 = ttk.Button(text="5", command=btn_click15)
    btn15.place(x=300, y=160, width = 60, height = 60)
    set_buttons()


    label3 = ttk.Label(text="Сколько взять:")
    label3.place(x = 370, y = 20)
    entry = ttk.Entry()
    entry.place(x=370, y = 40, width = 80)

    label1 = ttk.Label(text="Возможные перестановки:")
    label1.place(x = 20, y = 230)

    label2 = ttk.Label(text="Буфер:")
    label2.place(x = 20, y = 270)
    set_labels()

    label3 = ttk.Label(text="Перестановка:")
    label3.place(x = 370, y = 90)
    entry1 = ttk.Entry()
    entry1.place(x=370, y = 110, width = 30)
    entry2 = ttk.Entry()
    entry2.place(x=405, y = 110, width = 30)
    btn_mov = ttk.Button(text="Переставить", command=btn_mov_click)
    btn_mov.place(x=370, y=140, width = 80, height = 30)

    root.mainloop()