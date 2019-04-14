#Ejercicio resuelto a partir de la solución. Lo he ido creando como el ejemplo que vimos en clase, empezando por el formato y siguiendo
#por el funcionamiento. He ido comentando todas aquellas partes de aspectos que he tenido que analizar con más detalle porque no me resultaban evidentes
#de primeras y también he comentado aspectos que me ayuden a hacer una estructura mental de cómo programar.

from tkinter import *
from tkinter import ttk
import datetime
import calendar 

#Calendar hereda de ttk.Frame, esto es, tiene todos los métodos y propiedades de ttk.Frame.
class Date(ttk.Frame):
    __date__ = None
    __active__ = True
    __weekend__ = False
    __lblDate__ = None
    
    __activeColor__ = "#000000"
    __inactiveColor__ = "#c2c2c2"
    __weekendColor__ = "#FF6157"
    
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, width=76, height= 61, borderwidth=0.5, relief='groove')
        
        #Construimos la etiqueta, que hereda de ttk.Label
        self.__lblDate__ =ttk.Label(self, text="", font=('Arial', 28, 'bold'), width=2, anchor=E, foreground=self.__inactiveColor__)
        #Pintamos la etiqueta
        self.__lblDate__.place(x=37, y=22)
        
    def active(self, value=None):
        if value == None:
            return self.__active__
        elif value:
            self.__active__ = True
            if self.__weekend__:
                self.__lblDate__.config(foreground=self.__weekendColor__)
            else:
                self.__lblDate__.config(foreground=self.__activeColor__)
        else:
            self.__active__ = False
            self.__lblDate__.config(foreground=self.__inactiveColor__)
            
    def weekend(self, value=None):
        if value == None:
            return self.__weekend__
        elif value:
            self.__weekend__ = True
            if self.__active__:
                self.__lblDate__.config(foreground=self.__weekendColor__)
        else:
            self.__weekend__ = False
            self.active(self.__active__)
            
    def date(self, value=None):
        if value == None:
            return self.__date__
        else:
            self.__date__ = value
            self.__lblDate__.config(text=self.__date__.day)
            self.active(self.__active__)
            self.weekend(self.__weekend__)
            
    
#Calendar hereda de ttk.Frame, esto es, tiene todos los métodos y propiedades de ttk.Frame.
class Calendar(ttk.Frame):
    __month__ = None
    __days__ = []
    __cal__ = calendar.Calendar()
    
    #Creamos el inicializador y 'variabilizamos' el height y el width para poderlos utilizar posteriormente, con campos privados excepto el método month

    def __addMonth__(self, fecha, deltaMonth):
        mes = fecha.month
        year = fecha.year
        
        #El operador % me da el resto
        nMes = (fecha.month + deltaMonth) % 12
        
        if nMes == 0:
            nMes = 12
        
        #El operador '//' es la división entera
        nYear = fecha.year + (fecha.month + deltaMonth - 1) // 12
        return datetime.date(nYear, nMes, 1)

    def __init__(self, parent, **args):
        self.__width = args['width'] if 'width' in args else 532
        self.__height = args['height'] if 'height' in args else 422
        
        ttk.Frame.__init__(self, parent, width=self.__width, height=self.__height)
        self.__createHeader__()
        self.month()
        self.__createDays__()
        self.__setValuesDays__()
        self.__createDaysNames__()
        
        ix = 1
        for f in range(6):
            for c in range(7):
                d = self.__days__[c + f * 7]
                d.place(x=c*76, y=f*61+55)
    
    #Utilizamos el formato propagate para colocar las etiquetas de los días de la semana.            
    def __createDaysNames__(self):
        dias = ('Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo')
        for i in range(7):
            f = ttk.Frame(self, width=76, height=14)
            f.pack_propagate(0)
            ttk.Label(f, text=dias[i], font=('Arial', 11), anchor=CENTER, borderwidth=0.5, relief='groove').pack(fill=BOTH, expand=1)
            f.place(x=i*76, y=40)    
                
    def setMonth(self, delta):
        newMonth = self.__addMonth__(self.__month__, delta)
        self.month(newMonth.year, newMonth.month)
                
    def __createHeader__(self):
        self.header = ttk.Frame(self, width=self.__width, height = 40, borderwidth=0.5, relief='groove')
        self.header.place(x=0, y=0)
        
        self.__btnLastYear__ = ttk.Button(self.header, text="<<", width = 2, command=lambda: self.setMonth(-12))
        self.__btnLastYear__.place(x=24, y=8)
        self.__btnLastMonth__ = ttk.Button(self.header, text="<", width = 2, command=lambda: self.setMonth(-1))
        self.__btnLastMonth__.place(x=78, y=8)
        self.__lblMonth__=ttk.Label(self.header, text="", width=15, anchor=CENTER, font=('Arial', 28, 'bold'))
        self.__lblMonth__.place(x=146, y=0)
        self.__btnNextMonth__=ttk.Button(self.header, text=">", width=2, command=lambda: self.setMonth(+1))
        self.__btnNextMonth__.place(x=408, y=8)
        self.__btnLastYear__ = ttk.Button(self.header, text=">>", width = 2, command=lambda: self.setMonth(+12))
        self.__btnLastYear__.place(x=462, y=8)
        
    def __createDays__(self):
        for i in range(42):
            d = Date(self)
            if (i+2) % 7 == 0 or (i+1) % 7 == 0:
                d.weekend(True)
            self.__days__.append(d)
            
    def __setValuesDays__(self):
        if len(self.__days__) == 0:
            return
        
        #itermonthdates(year, month) Return an iterator for the month month (1–12) in the year year.
        #This iterator will return all days (as datetime.date objects) for the month and all days before the start of the month or
        #after the end of the month that are required to get a complete week.
        
        iMes = self.__cal__.itermonthdates(self.__month__.year, self.__month__.month)
        for ix, item in enumerate(iMes):
            self.__days__[ix].date(item)
            self.__days__[ix].active(item.month == self.__month__.month)
            maxDate = item
            
        if ix < 41:
            moreMonth = self.__addMonth__(self.__month__, 1)
            iMes = self.__cal__.itermonthdates(moreMonth.year, moreMonth.month)
            for item in iMes:
                if item > maxDate:
                    ix += 1
                    self.__days__[ix].date(item)
                    self.__days__[ix].active(item.month == self.__month__.month)
                    if ix >=41:
                        break
        
        
    def month(self, year=None, month=None):
        month_names = ('Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre')
        if year == None:
            self.__month__ = datetime.date.today()
        elif month == None:
            self.__month__ = datetime.date(year, 1, 1)
        else:
            self.__month__=datetime.date(year, month, 1)
                
        self.__lblMonth__.config(text="{} {}".format(month_names[self.__month__.month-1], self.__month__.year))
        self.__setValuesDays__()
                           
                        

#MainApp hereda de Tk (Tkinter), esto es, hereda todos los objetos de Tkinter, tiene acceso a todos sus objetos, con sus atributos y métodos.
class MainApp (Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("Calendario Universal")
        self.geometry("532x422")
        
        self.calendar = Calendar(self)
        self.calendar.place(x=0, y=0)
        
    def start(self):
        self.mainloop()
        
if __name__ == '__main__':
    app = MainApp()
    app.start()





