from tkinter import *
from tkinter import ttk
from Stock import Stock
import time
import random

def btn_mov_click():
    stock.movement()
    set_buttons()

def btn_add_click():
    stk = stock.get_db()
    for i in stk:
        if i[1] == 0:
            stock.add(i[0], rand_quant(10, 50), rand_type())
    set_buttons()

def rand_type():
    i = random.randint(1, 3)
    if i == 1:
        return "1"
    elif i == 2:
        return "2"
    else:
        return "3"

def rand_id():
    r = random.randint(1, 15)
    if r < 10:
        return '000'+str(r)
    else:
        return '00'+str(r)

def rand_quant(a, b):
    return random.randint(a, b)

def btn_start_click():
    n = 0
    while n < 30:
        while True:
            rand_cell = rand_id()
            rand_cell_quantity = stock.get_cell_quantity(rand_cell)
            if rand_cell_quantity > 0:
                rand_quantity = rand_quant(1, 10)
                stock.get(rand_cell, rand_quantity)
                break
        set_buttons()
        time.sleep(0.1)
        n += 1

def get_color(type):
    if type == '1':
        return "#87CEFA"
    elif type == '2':
        return "#98FB98"
    elif type == '3':
        return "#FFA07A"
    else:
        return "#A9A9A9"

def set_buttons():
    text = stock.get_db()
    btn1['text'] = str(text[0][1])
    btn1['background'] = get_color(text[0][2])
    btn2['text'] = str(text[1][1])
    btn2['background'] = get_color(text[1][2])
    btn3['text'] = str(text[2][1])
    btn3['background'] = get_color(text[2][2])
    btn4['text'] = str(text[3][1])
    btn4['background'] = get_color(text[3][2])
    btn5['text'] = str(text[4][1])
    btn5['background'] = get_color(text[4][2])
    btn6['text'] = str(text[5][1])
    btn6['background'] = get_color(text[5][2])
    btn7['text'] = str(text[6][1])
    btn7['background'] = get_color(text[6][2])
    btn8['text'] = str(text[7][1])
    btn8['background'] = get_color(text[7][2])
    btn9['text'] = str(text[8][1])
    btn9['background'] = get_color(text[8][2])
    btn10['text'] = str(text[9][1])
    btn10['background'] = get_color(text[9][2])
    btn11['text'] = str(text[10][1])
    btn11['background'] = get_color(text[10][2])
    btn12['text'] = str(text[11][1])
    btn12['background'] = get_color(text[11][2])
    btn13['text'] = str(text[12][1])
    btn13['background'] = get_color(text[12][2])
    btn14['text'] = str(text[13][1])
    btn14['background'] = get_color(text[13][2])
    btn15['text'] = str(text[14][1])
    btn15['background'] = get_color(text[14][2])


if  __name__ == "__main__":
    stock = Stock('stock.txt')
    root = Tk()     
    root.title("Склад")     
    root.geometry("460x240+540+270")    
    root.resizable(False, False)
   
    btn1 = ttk.Label(text="1")
    btn1.place(x=20, y=20, width = 60, height = 60)
    btn2 = ttk.Label(text="2")
    btn2.place(x=90, y=20, width = 60, height = 60)
    btn3 = ttk.Label(text="3")
    btn3.place(x=160, y=20, width = 60, height = 60)
    btn4 = ttk.Label(text="4")
    btn4.place(x=230, y=20, width = 60, height = 60)
    btn5 = ttk.Label(text="5")
    btn5.place(x=300, y=20, width = 60, height = 60)

    btn6 = ttk.Label(text="1")
    btn6.place(x=20, y=90, width = 60, height = 60)
    btn7 = ttk.Label(text="2")
    btn7.place(x=90, y=90, width = 60, height = 60)
    btn8 = ttk.Label(text="3")
    btn8.place(x=160, y=90, width = 60, height = 60)
    btn9 = ttk.Label(text="4")
    btn9.place(x=230, y=90, width = 60, height = 60)
    btn10 = ttk.Label(text="5")
    btn10.place(x=300, y=90, width = 60, height = 60)

    btn11 = ttk.Label(text="1")
    btn11.place(x=20, y=160, width = 60, height = 60)
    btn12 = ttk.Label(text="2")
    btn12.place(x=90, y=160, width = 60, height = 60)
    btn13 = ttk.Label(text="3")
    btn13.place(x=160, y=160, width = 60, height = 60)
    btn14 = ttk.Label(text="4")
    btn14.place(x=230, y=160, width = 60, height = 60)
    btn15 = ttk.Label(text="5")
    btn15.place(x=300, y=160, width = 60, height = 60)
    set_buttons()
    
    btn_start = ttk.Button(text="Старт", command=btn_start_click)
    btn_start.place(x=370, y=20, width = 80, height = 30)

    btn_add = ttk.Button(text="Заполнить", command=btn_add_click)
    btn_add.place(x=370, y=60, width = 80, height = 30)

    btn_mov = ttk.Button(text="Переставить", command=btn_mov_click)
    btn_mov.place(x=370, y=100, width = 80, height = 30)

    root.mainloop()