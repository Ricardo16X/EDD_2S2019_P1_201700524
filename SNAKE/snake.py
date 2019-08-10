import curses
import time

#Estructuras Importadas
import CircularDobleEnlazada

menu = ['1. Jugar', '2. Tabla de Punteo', '3. Selección Usuario', '4. Reportes', '5. Carga Masiva']
# Estructuras

listaCircularDoble = CircularDobleEnlazada.CDEnlazada()

def pintarMenu(stdscr, indexOpcion):
    stdscr.clear()
    h,w = stdscr.getmaxyx()
    for idx, row in enumerate(menu):
        x = w//2 - len(row)//2
        y = h//2 - len(menu)//2 + idx
        if(indexOpcion == idx):
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y,x,row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y,x,row)
        stdscr.refresh()

def registrarUsuario(stdscr):
    cadena = ""
    stdscr.clear()
    stdscr.refresh()
    h,w = stdscr.getmaxyx()
    registrar = "Ingresa tu Nombre: "
    x = w//2 - len(registrar)//2
    y = h//2 - len(registrar)//2        
    stdscr.addstr(y,x,registrar)
    stdscr.refresh()
    while True:
        key = stdscr.getkey()
        #if(key is not 10 or key is not curses.KEY_ENTER):
        if (key == '\n'):
            break
        else:
            cadena = cadena + key
            stdscr.addstr(y+1,x,cadena)
            stdscr.refresh()
    listaCircularDoble.ingresar(cadena)
    pintarMenu(stdscr, 0)
    

def main(stdscr):
    #Menu Inicial
    stdscr = curses.initscr()
    curses.curs_set(0)
    curses.noecho()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    opcionElegida = 0
    pintarMenu(stdscr, opcionElegida)
    while True:
        key = stdscr.getch()
        stdscr.clear()
        if (key == 450 or key == curses.KEY_UP) and opcionElegida > 0:
            opcionElegida -= 1
        elif (key == 456 or key == curses.KEY_DOWN) and opcionElegida < len(menu) - 1:
            opcionElegida += 1
        elif (key == 10 or key == curses.KEY_ENTER) or key == [10 - 13]:
            stdscr.clear()
            if opcionElegida is 2:
                registrarUsuario(stdscr)
            stdscr.refresh()
            stdscr.getch()
        elif key == 27 or key == curses.KEY_EXIT:
            break
        pintarMenu(stdscr, opcionElegida)
        stdscr.refresh()
        
curses.wrapper(main)