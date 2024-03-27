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
            otra_casilla.conexiones.append(self)

class Tablero:
    def __init__(self, archivo):
        with open(archivo, 'r') as f:
            lineas = f.readlines()
        self.tamaño = int(lineas[0].strip())
        self.casillas = [[Casilla(fila, columna) for columna in range(self.tamaño)] for fila in range(self.tamaño)]
        for linea in lineas[1:]:
            fila, columna, tipo_perla = map(int, linea.split(','))
            self.casillas[fila-1][columna-1].perla = Perla(tipo_perla)



class Aplicacion:
    def __init__(self, master, tablero):
        self.master = master
        self.tablero = tablero
        self.canvas = tk.Canvas(self.master, width=500, height=500)
        self.canvas.pack()
        self.dibujar_tablero()
        self.dibujar_lineas()

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

def main():
    archivo = 'file.txt'
    tablero = Tablero(archivo)
    root = tk.Tk()
    root.title("Juego Masyu")
    app = Aplicacion(root, tablero)
    root.mainloop()

if __name__ == "__main__":
    main()