import curses
import time

menu = ['1. Jugar', '2. Tabla de Punteo', '3. Selección Usuario', '4. Reportes', '5. Carga Masiva']

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

def main(stdscr):
    #Menu Inicial
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    opcionElegida = 0
    pintarMenu(stdscr, opcionElegida)
    while True:
        key = stdscr.getch()
        stdscr.clear()
        if key == 450 and opcionElegida > 0:
            opcionElegida -= 1
        elif key == 456 and opcionElegida < len(menu) - 1:
            opcionElegida += 1
        elif key == 10 or key == [10 - 13]:
            stdscr.clear()
            stdscr.addstr(0,0, "You pressed {}".format(menu[opcionElegida]))
            stdscr.refresh()
            stdscr.getch()
        
        pintarMenu(stdscr, opcionElegida)
        stdscr.refresh()
        
curses.wrapper(main)