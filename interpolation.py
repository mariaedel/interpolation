# import tkinter as tk
from tkinter import *
from tkinter.constants import BOTTOM
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
import matplotlib.pyplot as plt

def newton(x_uz, y_uz):
    a = x_uz[0]
    b = x_uz[-1]
    n = len(x_uz)-1
    x_poly = np.linspace(a, b, 100)
    A = y_uz.copy()

    for k in range(1, n+1):
        for i in range(0, n-k+1):
            A[i] = (A[i+1] - A[i]) / (x_uz[i+k] - x_uz[i])

    y_poly = A[0] * np.ones(x_poly.shape)

    for j in range(1, n+1):
        y_poly = A[j] + (x_poly - x_uz[j]) * y_poly

    return x_poly, y_poly

def spline(x_uz, y_uz):

    A = [0]
    B = [0]
    C = [0]
    x_spl = []
    y_spl = []

    a = x_uz[0]
    b = x_uz[-1]
    n = len(x_uz)-1

    d = (y_uz[1]-y_uz[0])/(x_uz[1]-x_uz[0])

    for i in range(1, n+1):
        if i == 1:
            left_part = np.array([[x_uz[i-1]**2, x_uz[i-1], 1], [x_uz[i]**2, x_uz[i], 1], [2, 0, 0]], dtype='float')
            right_part = np.array([[y_uz[i-1]], [y_uz[i]], [d]], dtype='float')

        else:
            left_part = np.array([[x_uz[i-1]**2, x_uz[i-1], 1], [x_uz[i]**2, x_uz[i], 1], [2*x_uz[i-1], 1, 0]], dtype='float')
            right_part = np.array([[y_uz[i-1]], [y_uz[i]], [2*A[i-1]*x_uz[i-1]+B[i-1]]], dtype='float')

        solution = np.linalg.solve(left_part, right_part)
        A.append(solution[0][0])
        B.append(solution[1][0])
        C.append(solution[2][0])
    
    for i in range(1, n+1):
        x = np.linspace(x_uz[i-1], x_uz[i], 100, dtype='float')
        spline = A[i] * x ** 2 + B[i] * x + C[i]

        x_spl = np.append(x_spl, x)
        y_spl = np.append(y_spl, spline)
    
    return x_spl, y_spl

class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.title('interpol')
        self.minsize(640, 400)
        lbl = Label(self, text='X')

        self.graph()

    def graph(self):
        f = plt.figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
        X1 = X.get().split()
        Y1 = Y.get().split()
        oX1 = oX.get()
        oY1 = oY.get()
        t = title.get()
               
        new_X = []
        new_Y = []
        for x in X1:
            new_X.append(float(x))
        for y in Y1:
            new_Y.append(float(y))

        x_poly, y_poly = newton(new_X, new_Y)
        a.plot(x_poly, y_poly)
        a.scatter(new_X, new_Y)

        if oX1 != '':
            plt.xlabel(oX1)

        if oY1 != '':
            plt.ylabel(oY1)

        if title != '':
            plt.title(t)

        plt.grid()

        canvas = FigureCanvasTkAgg(f, self)
        canvas.get_tk_widget().pack(side=BOTTOM, expand=True)

    
class Root1(Tk):
    def __init__(self):
        super(Root1, self).__init__()
        self.title('interpol')
        self.minsize(640, 400)
        lbl = Label(self, text='X')

        self.graph()

    def graph(self):
        f = plt.figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)

        X1 = X.get().split()
        Y1 = Y.get().split()

        oX1 = oX.get()
        oY1 = oY.get()
        t = title.get()
        
        new_X = []
        new_Y = []

        for x in X1:
            new_X.append(float(x))
        for y in Y1:
            new_Y.append(float(y))

        x_poly, y_poly = spline(new_X, new_Y)
        a.plot(x_poly, y_poly)
        a.scatter(new_X, new_Y)

        if oX1 != '':
            plt.xlabel(oX1)

        if oY1 != '':
            plt.ylabel(oY1)

        if title != '':
            plt.title(t)

        plt.grid()

        canvas = FigureCanvasTkAgg(f, self)
        # canvas.show()
        canvas.get_tk_widget().pack(side=BOTTOM, expand=True)

def graph1():
    if __name__ == '__main__':
        root = Root()
        root.mainloop()

def graph2():
    if __name__ == '__main__':
        root = Root1()
        root.mainloop()

window = Tk()
window.title("Интерполяция")  
window.geometry('220x370')  
lbl = Label(window, text="Введите значения Х и Y через пробел")  
lbl.grid(column=0, row=0) 
lbl_x = Label(window, text='X: (в порядке возрастания)')
lbl_x.grid(column=0, row=1) 
lbl_y = Label(window, text='Y: (соотетствующие значениям X)')
lbl_y.grid(column=0, row=3) 
X = Entry(window, width=30)
X.grid(column=0, row=2)
Y = Entry(window, width=30)
Y.grid(column=0, row=4)

_lbl_ = Label(window, text=" ")  
_lbl_.grid(column=0, row=5)

lbl1 = Label(window, text="Введите название оси oX")  
lbl1.grid(column=0, row=6) 
oX = Entry(window, width=30)
oX.grid(column=0, row=7)

lbl2 = Label(window, text="Введите название оси oY")  
lbl2.grid(column=0, row=8)
oY = Entry(window, width=30)
oY.grid(column=0, row=9)

lbl3 = Label(window, text="Введите название графика")  
lbl3.grid(column=0, row=10)
title = Entry(window, width=30)
title.grid(column=0, row=11)

lbl_ = Label(window, text=" ")  
lbl_.grid(column=0, row=12)
lbl__ = Label(window, text=" ")  
lbl__.grid(column=0, row=13)

btn1 = Button(window, text="Построить интерполяционный\nполином Ньютона", command=graph1)  
btn1.grid(column=0, row=14)  
btn2 = Button(window, text="Построить сплайн", command=graph2)  
btn2.grid(column=0, row=15)  

if __name__ == '__main__':
    window.mainloop()

