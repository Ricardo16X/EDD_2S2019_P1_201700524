import curses
from curses import textpad
import time
from random import randint
#Estructuras Importadas
import CircularDobleEnlazada
import Pila
import Cola
import EnlazadaDoble

menu = ['1. Jugar', '2. Tabla de Punteo', '3. Selección Usuario', '4. Reportes', '5. Carga Masiva']

# Estructuras
nuevaPila = Pila.Pila()
nuevaCola = Cola.Cola()
usuarios = CircularDobleEnlazada.CDEnlazada()
serpiente = EnlazadaDoble.listaDE()
## Aqui funcionará el juego
def pintarJuego(stdscr, nombreUsuario):
    if nombreUsuario is "":
        registrarUsuario(stdscr)
    else:
        stdscr.clear()
        stdscr.nodelay(1)
        stdscr.timeout(150)
        punteo = 0
        nivel = 1
        alto, ancho = stdscr.getmaxyx()
        stdscr.addstr(1,25 - len("Puntaje"),"Puntaje = " + str(punteo))
        stdscr.addstr(1,50 - len("Nivel"),"Nivel = " + str(nivel))
        stdscr.addstr(1,75 - len("Usuario"),"Usuario = " + str(nombreUsuario))
        randomY = randint(3,alto-3)
        randomX = randint(3,ancho - 4)
        comidita = "*"
        stdscr.addstr(randomY, randomX, comidita)
        stdscr.border(0)
        textpad.rectangle(stdscr, 2, 2, alto - 2, ancho - 3)
        # Inserto el cuerpo inicial de la serpiente
        serpiente.insertar(alto//2, ancho//2 - 1)
        serpiente.insertar(alto//2, ancho//2)
        serpiente.insertar(alto//2, ancho//2 + 1)
        # Fin creación de serpiente
        # temporal para recorrer la serpiente y dibujar sus coordenadas
        temporalSerpiente = serpiente.ancla
        key = 452
        keyAnterior = key
        direccion = curses.KEY_LEFT
        while temporalSerpiente.siguiente is not None:
            temporalSerpiente = temporalSerpiente.siguiente
            stdscr.addstr(int(str(temporalSerpiente.cY)), int(str(temporalSerpiente.cX)), "#")
        stdscr.refresh()
        while True:
            temporal = serpiente.ancla.siguiente
            tempCX = 0
            tempCY = 0

            if key > 0:
                keyAnterior = key
                print(keyAnterior)
            
            key = stdscr.getch()
            print(key)
            #He creado esta restricción, ya que no se me ocurre como voltear a la serpiente
            # cuando esta sea muy larga y tenga muchos dobleces
            if key in [curses.KEY_UP, 450] and (keyAnterior in [curses.KEY_DOWN, 456]):
                key = keyAnterior
            elif key in [curses.KEY_DOWN, 456] and keyAnterior in [curses.KEY_UP, 450]:
                key = keyAnterior
            elif key in [curses.KEY_LEFT, 452] and keyAnterior in [curses.KEY_RIGHT, 454]:
                key = keyAnterior
            elif key in [curses.KEY_RIGHT, 454] and keyAnterior in [curses.KEY_LEFT, 452]:
                key = keyAnterior

            stdscr.clear()
            if key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT] or key in [450, 456, 452, 454]:
                direccion = key
            
            if temporal.cX == randomX and temporal.cY == randomY:
                print(comidita)
                if comidita is "+":
                    serpiente.insertar(0,0)
                    punteo += 1
                else:
                    serpiente.eliminar()
                    if punteo > 0:
                        punteo -= 1

                randomX = randint(3, ancho - 4)
                randomY = randint(3, alto - 3)
                crecer_o_disminuir = randint(0,10)

                if crecer_o_disminuir >= 0 and crecer_o_disminuir <= 6:
                    comidita = "+"
                    stdscr.addstr(randomY, randomX, comidita)
                else:
                    comidita = "*"
                    stdscr.addstr(randomY, randomX, comidita)
            else:
                stdscr.addstr(randomY, randomX, comidita)

            if direccion in [curses.KEY_UP, 450]:
                tempCX = temporal.cX
                tempCY = temporal.cY
                temporal.cY -= 1
                if temporal.cY <= 2:
                    tempCY = alto - 3
                    serpiente.actualizar(tempCX,tempCY)
            elif direccion in [curses.KEY_DOWN, 456]:
                tempCX = temporal.cX
                tempCY = temporal.cY
                temporal.cY += 1
                if temporal.cY >= alto - 2:
                    tempCY = 3
                    serpiente.actualizar(tempCX,tempCY)
            elif direccion in [curses.KEY_LEFT, 452]:
                tempCX = temporal.cX
                tempCY = temporal.cY
                temporal.cX -= 1
                if temporal.cX <= 2:
                    tempCX = ancho - 5
                    serpiente.actualizar(tempCX,tempCY)
            elif direccion in [curses.KEY_RIGHT, 454]:
                tempCX = temporal.cX
                tempCY = temporal.cY
                temporal.cX += 1
                if temporal.cX >= ancho - 4:
                    tempCX = 3
                    serpiente.actualizar(tempCX,tempCY)
            serpiente.actualizar(tempCX,tempCY)
            
            alto, ancho = stdscr.getmaxyx()
            stdscr.addstr(1,25 - len("Puntaje"),"Puntaje = " + str(punteo))
            stdscr.addstr(1,50 - len("Nivel"),"Nivel = " + str(nivel))
            stdscr.addstr(1,75 - len("Usuario"),"Usuario = " + str(nombreUsuario))
            stdscr.border(0)
            textpad.rectangle(stdscr, 2, 2, alto - 2, ancho - 3)
            while temporal is not None:
                stdscr.addstr(int(str(temporal.cY)), int(str(temporal.cX)), str(temporal.char))
                temporal = temporal.siguiente
            stdscr.refresh()
            
    
## Será el apartado para dibujar el menú inicial
def pintarMenuInicial(stdscr, opcionElegida):
    # despinto la pantalla
    stdscr.clear()
    # Obtenemos el tamaño máximo de la pantalla
    alto, ancho = stdscr.getmaxyx()
    for index, fila in enumerate(menu):
        x = ancho//2 - 20
        y = alto//2 - len(menu)//2 + index
        if(opcionElegida == index):
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y,x,fila)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y,x,fila)
        stdscr.addstr(1,1,"ESC Salir")
        stdscr.refresh()
## Servirá para elegir el personaje en el menú seleccionado
def elegirPersonaje(stdscr):
    #Contamos el numero de jugadores registrados
    numero = usuarios.cantidad()
    if numero > 0:
        # Hay jugadores, muestro el siguiente menu
        stdscr.clear()
        alto, ancho = stdscr.getmaxyx()
        x = ancho//2 - len("Elige tu Nombre")
        y = alto//2 - 2
        stdscr.addstr(1,1,"ESC Salir")
        stdscr.addstr(y,x,"Elige tu Nombre")
        # While para que sea mientras presione un boton
        while True:
            tecla = stdscr.getch()
            stdscr.clear()
            if tecla == curses.KEY_LEFT or tecla == 452:
                # Pediré el usuario que está a la izquierda o sea al anterior del actual y lo mostraré en pantalla
                nombreJugador = usuarios.jugador("L")
            elif tecla == curses.KEY_RIGHT or tecla == 454:
                # Pediré el usuario que está a la derecha o siguiente del actual
                nombreJugador = usuarios.jugador("R")
            elif tecla == 10 or tecla == curses.KEY_ENTER:
                # El usuario ha tecleado el Enter, entonces ha seleccionado un jugador
                # el juego empieza con el nombre del jugador seleccionado
                '''Falta agregar la funcionalidad del juego'''
                pintarJuego(stdscr, nombreJugador)
                pintarMenuInicial(stdscr, 0)
                break
            elif tecla == 27 or tecla == curses.KEY_ABORT:
                # Al usuario que pulse ESC se le mostrará el menu de inicio.
                break
            # Muestro el nombre de manera mucho más corta
            stdscr.addstr(1,1,"ESC Salir")
            stdscr.addstr(y,x,"Elige tu Nombre")
            xnomJug = ancho//2 - len("Elige tu Nombre")
            ynomJug = alto//2
            stdscr.addstr(ynomJug, xnomJug,"<--   "+ nombreJugador +"   -->")
            stdscr.refresh()
        pintarMenuInicial(stdscr, 3)
    else:
        #No hay jugadores, muestro el menu de registro
        registrarUsuario(stdscr)

def registrarUsuario(stdscr):
    stdscr.clear()
    alto, ancho = stdscr.getmaxyx()
    x = ancho//2 - len("Ingresa tu Nombre:")
    y = alto//2
    stdscr.addstr(1,1,"ESC Salir")
    stdscr.addstr(y, x, "Ingresa tu Nombre:")
    nombreIngresado = ""
    # un While para pedir los caracteres del nombre
    while True:
        tecla = stdscr.getkey()
        if tecla is not "\n":
            stdscr.clear()
            # Voy a mostrar un mensaje que me pida el nombre
            stdscr.addstr(y, x, "Ingresa tu Nombre:")
            nombreIngresado += tecla
            xnom = ancho//2 - len("Ingresa tu Nombre:")
            ynom = alto//2 + 2
            stdscr.addstr(ynom,xnom,nombreIngresado)
            stdscr.refresh()
        else:
            ## Vamos a registrar el nombre ingresado por el usuario
            usuarios.ingresar(nombreIngresado)
            pintarJuego(stdscr, nombreIngresado)
            break
## Inicio de juego de verdad
## Primero comenzaré con el diseño del Menú Inicial
def menuInicial(stdscr):
    stdscr = curses.initscr()
    curses.curs_set(0)
    curses.noecho()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    opcion = 0
    ## Pintaremos el menú para mostrarlo xd
    pintarMenuInicial(stdscr, opcion)
    while True:
        ## Pediremos al Usuario una opcion dependiendo de la tecla
        tecla = stdscr.getch()
        # Limpiaremos la pantalla de consola
        stdscr.clear()
        ## Ahora verificamos que tecla pulso el usuario
        if tecla == 450 or tecla == curses.KEY_UP and opcion > 0:
            opcion -= 1
        elif tecla == 456 or tecla == curses.KEY_DOWN and opcion < len(menu) - 1:
            opcion += 1
        elif tecla == 10 or tecla == curses.KEY_ENTER:
            ## Limpiaremos primero la pantalla para mostrar el siguiente
            stdscr.clear()
            ## Aqui reconocemos que el usuario ha pulsado enter
            # Por lo tanto veremos en que "opcion" hizo enter
            if opcion is 0:
                # Mostraremos el juego como tal
                pintarJuego(stdscr, "")
            elif opcion is 1:
                # Mostraremos la tabla de puntaje
                mostrarTablaPuntaje(stdscr)
            elif opcion is 2:
                # Mostraremos el menú para elegir "personaje"
                elegirPersonaje(stdscr)
            elif opcion is 3:
                # Mostraremos el menú para los reportes
                menuReportes(stdscr)
            elif opcion is 4:
                # Mostraremos el menú para el llenado masivo
                llenadoMasivo(stdscr)
        elif tecla == 27 or tecla == curses.KEY_ABORT:
            # Si el usuario pulsa ESC en el menu inicial, se saldrá del programa
            break
        pintarMenuInicial(stdscr, opcion)
curses.wrapper(menuInicial)