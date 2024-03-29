import curses
from curses import textpad
from random import randint
import csv
#Estructuras Importadas
import CircularDobleEnlazada
import Pila
import Cola
import EnlazadaDoble

menu = ['1. Jugar', '2. Tabla de Punteo', '3. Selección Usuario', '4. Reportes', '5. Carga Masiva']
reportes = ['1. Punteos', '2. Usuarios']
# Estructuras
userScoreReport = Cola.Cola()
usuarios = CircularDobleEnlazada.CDEnlazada()
## Aqui funcionará el juego
def pintarJuego(stdscr, nombreUsuario):
    if nombreUsuario is "":
        registrarUsuario(stdscr)
    else:
        serpiente = EnlazadaDoble.listaDE()
        score = Pila.Pila()
        stdscr.clear()
        velocidad = 150
        punteo = 0
        nivel = 1
        #Punteo de cambio de nivel
        pt = 5
        quitar = 50
        stdscr.timeout(velocidad)
        alto, ancho = stdscr.getmaxyx()
        stdscr.addstr(1 , 1 ,"Puntaje = " + str(punteo))
        stdscr.addstr(1 , ancho//2,"Nivel = " + str(nivel))
        stdscr.addstr(1 , ancho - len("Usuario"),"Usuario = " + str(nombreUsuario))
        randomY = randint(3,alto-3)
        randomX = randint(3,ancho - 4)
        comidita = "+"
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
        # Bucle del Juego
        colision_sinComida = False
        Pausa = False
        while True:
            if punteo == pt and velocidad > 25 and nivel < 3:
                nivel += 1
                pt = pt + 5
                velocidad = velocidad - quitar
                quitar += 40
                stdscr.timeout(velocidad)
            temporal = serpiente.ancla.siguiente
            tempCX = 0
            tempCY = 0

            if key > 0:
                keyAnterior = key
            
            key = stdscr.getch()
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
            elif key in [curses.KEY_ABORT, 27]:
                #Boton de Pausa
                if Pausa is False:
                    Pausa = True
                else:
                    Pausa = False
            
            if temporal.cX == randomX and temporal.cY == randomY:
                ## Agrego los valores a la pila para el score result
                score.push(randomX, randomY)
                ## Luego creo el reporte del mismo
                score.graficar()
                #################################
                if comidita is "+":
                    serpiente.insertar(0,0)
                    colision_sinComida = False
                    punteo += 1
                elif comidita is "*":
                    serpiente.eliminar()
                    colision_sinComida = False
                    serpiente.actualizar(temporal.cX,temporal.cY)
                    if punteo > 0:
                        punteo -= 1
                #################################
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
            
            if Pausa is False:
                if direccion in [curses.KEY_UP, 450]:
                    # Lo que haré aquí será atravesar la pared
                    # por medio de la cabeza del snake
                    if temporal.cY <= 3:
                        temporal.cY = alto-3
                    else:
                        tempCX = temporal.cX
                        tempCY = temporal.cY
                        temporal.cY -= 1
                elif direccion in [curses.KEY_DOWN, 456]:
                    if temporal.cY >= alto - 3:
                        temporal.cY = 3
                    else:
                        tempCX = temporal.cX
                        tempCY = temporal.cY
                        temporal.cY += 1    
                elif direccion in [curses.KEY_LEFT, 452]:
                    if temporal.cX <= 3:
                        temporal.cX = ancho - 4
                    else:
                        tempCX = temporal.cX
                        tempCY = temporal.cY
                        temporal.cX -= 1
                elif direccion in [curses.KEY_RIGHT, 454]:
                    if temporal.cX >= ancho - 4:
                        temporal.cX = 3
                    else:
                        tempCX = temporal.cX
                        tempCY = temporal.cY
                        temporal.cX += 1
                serpiente.actualizar(tempCX,tempCY)
                
                if colision_sinComida == False:
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
                    colision_sinComida = serpiente.colision(True)
                else:
                    serpiente.generarReporte()
                    userScoreReport.push(nombreUsuario,punteo)
                    serpiente.cantidad = 0
                    punteo = 0
                    serpiente.vaciarSerpiente()
                    stdscr.clear()
                    stdscr.timeout(-1)
                    alto, ancho = stdscr.getmaxyx()
                    stdscr.addstr(alto//2, ancho//2 - len("GAME OVER"), "GAME OVER")
                    stdscr.addstr(alto//2 + 1, ancho//2 - len("Presiona una tecla para continuar..."), "Presiona una tecla para continuar...")
                    stdscr.refresh()
                    stdscr.getch()
                    break
            else:
                serpiente.generarReporte()
                stdscr.clear()
                stdscr.addstr(alto//2,ancho//2 - len("PAUSA"),"PAUSA")
                stdscr.refresh()
## Mostraremos el Score actual en tabla
def mostrarTablaPuntaje(stdscr):
    stdscr.clear()
    stdscr.border(0)
    alto, ancho = stdscr.getmaxyx()
    temporal = userScoreReport
    temporalito = userScoreReport.ancla
    if temporal.numeroPunteos > 0:
        y = 5
        stdscr.addstr(y, ancho//4, "Nombre")
        stdscr.addstr(y, ancho//2, "Punteo")
        while temporalito.siguiente is not None:
            y = y + 1
            temporalito = temporalito.siguiente
            stdscr.addstr(y, ancho//4, temporalito.nombre)
            stdscr.addstr(y, ancho//2, str(temporalito.puntuacion))
    else:
        stdscr.addstr(alto//2, ancho//2 - len("NO HAY PUNTEOS QUE MOSTRAR"), "NO HAY PUNTEOS QUE MOSTRAR")
    stdscr.refresh()
    stdscr.getch()
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
def pintarMenuReportes(stdscr, opcionElegida):
    # despinto la pantalla
    stdscr.clear()
    # Obtenemos el tamaño máximo de la pantalla
    alto, ancho = stdscr.getmaxyx()
    for index, fila in enumerate(reportes):
        x = ancho//2 - 20
        y = alto//2 - len(reportes)//2 + index
        if(opcionElegida == index):
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y,x,fila)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y,x,fila)
    stdscr.addstr(2,2,"ESC Salir")
    stdscr.addstr(alto//2 - 5, ancho//2 - len("REPORTES"), "REPORTES")
    stdscr.refresh()
## Pintar menu de repotes
def menuReportes(stdscr):
    stdscr.border(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    opcion = 0
    pintarMenuReportes(stdscr, opcion)
    while True:
        tecla = stdscr.getch()
        if tecla == 450 or tecla == curses.KEY_UP and opcion > 0:
            opcion -= 1
        elif tecla == 456 or tecla == curses.KEY_DOWN and opcion < len(reportes) - 1:
            opcion += 1
        elif tecla == 10 or tecla == curses.KEY_ENTER:
            ## Limpiaremos primero la pantalla para mostrar el siguiente
            stdscr.clear()
            ## Aqui reconocemos que el usuario ha pulsado enter
            # Por lo tanto veremos en que "opcion" hizo enter
            if opcion is 0:
                # Mostraremos el juego como tal
                userScoreReport.graficar()
            elif opcion is 1:
                # Mostraremos la tabla de puntaje
                usuarios.graficar()
        elif tecla == 27 or tecla == curses.KEY_ABORT:
            # Si el usuario pulsa ESC en el menu inicial, se saldrá del programa
            break
        pintarMenuReportes(stdscr, opcion)
# Ingreso de archivo .csv
def llenadoMasivo(stdscr):
    stdscr.clear()
    stdscr.addstr(1,1, "ESC - Salir")
    stdscr.addstr(2,1,"Carga Masiva _ Archivos CSV")
    stdscr.addstr(3,1,"Funcionamiento:")
    stdscr.addstr(4,1,"Coloca el archivo .csv en la carpeta del juego")
    stdscr.addstr(5,1,"Escribe el nombre del archivo:")
    cadenaTexto = ""
    while True:
        tecla = stdscr.getkey()
        stdscr.clear()
        if tecla is "\n":
            try:
                i = 0
                nNombre = 1
                archivo = open(cadenaTexto, "r", newline="")
                for linea in archivo:
                    dato = linea.split(",\r\n")
                    dato.append(dato)
                    for nombre in dato:
                        if i%3 == 0 and nNombre is not 1:
                            usuarios.ingresar(nombre)
                        i = i + 1
                        nNombre = nNombre + 1
                break
            except Exception:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(0,1,"Ha ocurrido un error, intentalo nuevamente :/")
                stdscr.attroff(curses.color_pair(1))
        elif tecla is "\x08":
            cadenaTexto = cadenaTexto[0:len(cadenaTexto) - 1]
        elif tecla is "\x1b":
            break
        else:
            cadenaTexto = cadenaTexto + tecla
        stdscr.addstr(1,1, "ESC - Salir")
        stdscr.addstr(2,1,"Carga Masiva _ Archivos CSV")
        stdscr.addstr(3,1,"Funcionamiento:")
        stdscr.addstr(4,1,"Coloca el archivo .csv en la carpeta del juego")
        stdscr.addstr(5,1,"Escribe el nombre del archivo:")
        stdscr.addstr(6,1,cadenaTexto)
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
        stdscr.addstr(y + 1,x - len(usuarios.ancla.siguiente.nombre),"<--   " + usuarios.ancla.siguiente.nombre + "   -->")
        # While para que sea mientras presione un boton
        while True:
            tecla = stdscr.getch()
            stdscr.clear()
            if tecla == curses.KEY_LEFT or tecla == 452 or tecla == curses.KEY_UP or tecla == 450:
                # Pediré el usuario que está a la izquierda o sea al anterior del actual y lo mostraré en pantalla
                nombreJugador = usuarios.jugador("L")
            elif tecla == curses.KEY_RIGHT or tecla == 454 or tecla == curses.KEY_DOWN or tecla == 456:
                # Pediré el usuario que está a la derecha o siguiente del actual
                nombreJugador = usuarios.jugador("R")
            elif tecla == 10 or tecla == curses.KEY_ENTER:
                # El usuario ha tecleado el Enter, entonces ha seleccionado un jugador
                # el juego empieza con el nombre del jugador seleccionado
                pintarJuego(stdscr, nombreJugador)
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
    else:
        #No hay jugadores, muestro el menu de registro
        registrarUsuario(stdscr)


        # Menu para registrar un usuario
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
        if tecla is "\x08":
            nombreIngresado = nombreIngresado[0:len(nombreIngresado) - 1]
        if tecla is "\n":
            ## Vamos a registrar el nombre ingresado por el usuario
            usuarios.ingresar(nombreIngresado)
            pintarJuego(stdscr, nombreIngresado)
            break
        elif tecla is "\x1b":
            break
        else:
            stdscr.clear()
            # Voy a mostrar un mensaje que me pida el nombre
            stdscr.addstr(y, x, "Ingresa tu Nombre:")
            nombreIngresado += tecla
            xnom = ancho//2 - len("Ingresa tu Nombre:")
            ynom = alto//2 + 2
            stdscr.addstr(ynom,xnom,nombreIngresado)
            stdscr.refresh()
## Inicio de juego de verdad
## Primero comenzaré con el diseño del Menú Inicial
def menuInicial(stdscr):
    stdscr = curses.initscr()
    curses.curs_set(0)
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