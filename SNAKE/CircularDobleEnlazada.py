import os
#reporte de usuarios registrados en el juego
class nodoCDEnlazada():
    def __init__(self,nombre):
        self.nombre = nombre
        self.siguiente = None
        self.anterior = None
        
class CDEnlazada():
    def __init__(self):
        self.ancla = nodoCDEnlazada(None)
        self.ultimo = self.ancla
        self.primero = None
        self.temporalTeclas = self.ancla
        self.numeroElementos = 0
        
    def ingresar(self, nombreUsuario):
        temporal = self.ancla
        #Creaci�n de nuevo nodo
        nuevoRegistroUsuario = nodoCDEnlazada(nombreUsuario)
        self.numeroElementos += 1
        if temporal.siguiente is None:
            # Es el primer elemento de la lista circular doble
            temporal.siguiente = nuevoRegistroUsuario
            temporal.anterior = nuevoRegistroUsuario
            self.primero = self.ultimo = nuevoRegistroUsuario
            self.ultimo.siguiente = self.primero
            self.primero.anterior = self.ultimo
        else:
            #Lo voy a manejar que ingrese de ultimo
            tempUltimo = self.ultimo
            self.ultimo = nuevoRegistroUsuario
            # Intercambiamos punteros
            tempUltimo.siguiente = self.ultimo
            self.ultimo.anterior = tempUltimo
            ## Apuntamos al Inicio y al Final
            self.ultimo.siguiente = self.primero
            self.primero.anterior = self.ultimo

    def cantidad(self):
        return self.numeroElementos

    def jugador(self, tecla):
        if tecla is "R":
            self.temporalTeclas = self.temporalTeclas.siguiente
            return self.temporalTeclas.nombre
        elif tecla is "L":
            self.temporalTeclas = self.temporalTeclas.anterior
            return self.temporalTeclas.nombre
     
    def graficar(self):
        if self.numeroElementos > 0:
            archivo = open("usuarios.dot","w")
            archivo.write("digraph G{\n")
            archivo.write("rankdir = \"LR\"\n")
            archivo.write("node [shape = record];\n")
            temporal = self.ancla.siguiente
            numeroNodo = 1
            while True:
                archivo.write("n" + str(numeroNodo)  + "[shape=record, label=\"{| " + temporal.nombre + " |}\"]\n")
                temporal = temporal.siguiente
                numeroNodo += 1
                if temporal is self.ancla.siguiente:
                    break
            numeroNodo -= 1
            i = 1
            # While de relaciones
            archivo.write("n1 -> n" + str(numeroNodo) + "\n")
            archivo.write("n" + str(numeroNodo) + " -> n1 \n")
            while i < numeroNodo:
                archivo.write("n" + str(i) + " -> n" + str(i+1) + "\n" )
                archivo.write("n" + str(i+1) + " -> n" + str(i) + "\n" ) 
                i = i + 1
            archivo.write("}")
            archivo.close()
            os.system("dot -Tjpg usuarios.dot -o reporteUsuarios.jpg")
        