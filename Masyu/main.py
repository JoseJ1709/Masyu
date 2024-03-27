import tkinter as tk


class Perla:
    def __init__(self, tipo):
        self.tipo = tipo


class Casilla:
    def __init__(self, fila, columna, perla=None):
        self.fila = fila
        self.columna = columna
        self.perla = perla
        self.linea = None
        self.conexiones = []

    def esta_vacia(self):
        return self.perla is None and self.linea is None

    def conectar_con(self, otra_casilla):
        if otra_casilla not in self.conexiones:
            self.conexiones.append(otra_casilla)
            self.linea = True
            otra_casilla.conexiones.append(self)
            otra_casilla.linea = True


class Tablero:
    def __init__(self, archivo):
        with open(archivo, 'r') as f:
            lineas = f.readlines()
        self.tamaño = int(lineas[0].strip())
        self.casillas = [[Casilla(fila, columna) for columna in range(self.tamaño)] for fila in range(self.tamaño)]
        for linea in lineas[1:]:
            fila, columna, tipo_perla = map(int, linea.split(','))
            self.casillas[fila-1][columna-1].perla = Perla(tipo_perla)

    def reglas_lineas(self,casilla1,casilla2):
        #revisar que las caillas que quieras conectar esten en la misma fila o columna
        revisarD = self.casillas[casilla1.fila+1][casilla1.columna]
        revisarI = self.casillas[casilla1.fila-1][casilla1.columna]
        revisarA = self.casillas[casilla1.fila][casilla1.columna+1]
        revisarB = self.casillas[casilla1.fila][casilla1.columna-1]
        if revisarD == casilla2 or revisarI == casilla2 or revisarA == casilla2 or revisarB == casilla2:
            print("Se puede conectar lineas check basico")
            return True
        else:
            print("No se puede conectar lineas check basico")
            return False
    def reglas_perlas(self,casilla1,casilla2):
        #revisar si hay dos lineas conectadas en las casillas que se quieren conectar
        if len(casilla1.conexiones) >= 2 or len(casilla2.conexiones) >= 2:
            print("No se puede conectar lineas, Mas de dos lineas conectadas")
            return False
        #se puede agregar una conexion a las casillas
        if(casilla1.perla is None and casilla2.perla is None):
            print("Se puede conectar lineas No hay perlas en las casillas")
            return True
        else:
            #si la casilla tiene una perla negra
            if casilla1.perla is not None and casilla1.perla.tipo == 2:
                if(casilla1.columna == casilla2.columna or casilla1.fila == casilla2.fila):
                    if(casilla1.columna  == casilla2.columna):
                        revisar1 = self.casillas[casilla1.fila - 1][casilla1.columna]
                        revisar2 = self.casillas[casilla1.fila + 1][casilla1.columna]
                        if(revisar1.linea or revisar2.linea):
                            print("No se puede conectar linea en filas adyacentes, Perla Negra")
                            return False
                        else:
                            print("Se puede conectar linea en filas adyacentes, Perla Negra")
                            return True
                    if(casilla1.fila == casilla2.fila):
                        revisar1 = self.casillas[casilla1.fila][casilla1.columna - 1]
                        revisar2 = self.casillas[casilla1.fila][casilla1.columna + 1]
                        if(revisar1.linea or revisar2.linea):
                            print("No se puede conectar linea en columnas adyacentes, Perla Negra")
                            return False
                        else:
                            print("Se puede conectar linea, Perla Negra")
                            return True

            #si la casilla tiene perla Blanca
            if casilla1.perla is not None and casilla1.perla.tipo == 1:
                if (casilla1.columna == casilla2.columna or casilla1.fila == casilla2.fila):
                    if (casilla1.columna == casilla2.columna):
                        revisar1 = self.casillas[casilla1.fila][casilla1.columna+1]
                        revisar2 = self.casillas[casilla1.fila][casilla1.columna-1]
                        if (revisar1.linea or revisar2.linea):
                            print("No se puede conectar linea con filas adyacentes, Perla Blanca")
                            return False
                        else:
                            print("Se puede conectar linea, Perla Blanca ")
                            return True
                    if (casilla1.fila == casilla2.fila):
                        revisar1 = self.casillas[casilla1.fila + 1][casilla1.columna]
                        revisar2 = self.casillas[casilla1.fila - 1][casilla1.columna]
                        if (revisar1.linea or revisar2.linea):
                            print("No se puede conectar linea con columnas adyacentes, Perla Blanca")
                            return False
                        else:
                            print("Se puede conectar linea, Perla Blanca")
                            return True
            else:
                return True

class Aplicacion:
    def __init__(self, master, tablero):
        self.master = master
        self.tablero = tablero
        self.canvas = tk.Canvas(self.master, width=500, height=500)
        self.canvas.pack()
        self.dibujar_tablero()
        self.dibujar_lineas()
        self.casilla_seleccionada = None
        self.canvas.bind("<Button-1>", self.manejar_clicks)

    def dibujar_tablero(self):
        paso = 500 / self.tablero.tamaño
        for fila in range(self.tablero.tamaño):
            for columna in range(self.tablero.tamaño):
                casilla = self.tablero.casillas[fila][columna]
                if casilla.perla:
                    x0 = columna * paso
                    y0 = fila * paso
                    if casilla.perla.tipo == 1:
                        color = 'white'
                    else:
                        color = 'black'
                    self.canvas.create_oval(x0 + paso*0.25, y0 + paso*0.25, x0 + paso*0.75, y0 + paso*0.75, fill=color)
    def dibujar_lineas(self):
        paso = 500 / self.tablero.tamaño
        for i in range(self.tablero.tamaño):
            self.canvas.create_line(i * paso, 0, i * paso, 500)
            self.canvas.create_line(0, i * paso, 500, i * paso)
    def manejar_clicks(self, event):
        fila = int(event.y / (500 / self.tablero.tamaño))
        columna = int(event.x / (500 / self.tablero.tamaño))
        casilla_clicada = self.tablero.casillas[fila][columna]
        if self.casilla_seleccionada is None:
            self.casilla_seleccionada = casilla_clicada
        else:
            if self.tablero.reglas_lineas(self.casilla_seleccionada, casilla_clicada) and self.tablero.reglas_perlas(self.casilla_seleccionada, casilla_clicada):
                self.casilla_seleccionada.conectar_con(casilla_clicada)
                self.dibujar_linea(self.casilla_seleccionada, casilla_clicada)
            else:
                if(self.casilla_seleccionada.perla != None or casilla_clicada.perla != None):
                    self.dibujar_perla_roja(self.casilla_seleccionada)
                    self.dibujar_linea(self.casilla_seleccionada, casilla_clicada)
                else:
                    print("No se puede conectar lineas")
            self.casilla_seleccionada = None
    def dibujar_linea(self, casilla1, casilla2):
        paso = 500 / self.tablero.tamaño
        x1 = casilla1.columna * paso + paso / 2
        y1 = casilla1.fila * paso + paso / 2
        x2 = casilla2.columna * paso + paso / 2
        y2 = casilla2.fila * paso + paso / 2
        self.canvas.create_line(x1, y1, x2, y2)
    def dibujar_perla_roja(self, casilla):
        paso = 500 / self.tablero.tamaño
        x0 = casilla.columna * paso
        y0 = casilla.fila * paso
        self.canvas.create_oval(x0 + paso*0.25, y0 + paso*0.25, x0 + paso*0.75, y0 + paso*0.75, fill='red')
def main():
    archivo = 'file.txt'
    tablero = Tablero(archivo)
    root = tk.Tk()
    root.title("Juego Masyu")
    app = Aplicacion(root, tablero)
    root.mainloop()

if __name__ == "__main__":
    main()