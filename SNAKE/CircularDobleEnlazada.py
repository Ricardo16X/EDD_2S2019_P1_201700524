#reporte de usuarios registrados en el juego
class nodoCDEnlazada():
    def __init__(self,nombre):
        self.nombre = nombre
        self.siguiente = None
        self.anterior = None
        
class CDEnlazada():
    numeroElementos = 0
    def __init__(self):
        self.ancla = nodoCDEnlazada(None)
        self.ultimo = self.ancla
        self.primero = None
        self.temporalTeclas = self.ancla
        
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
        
            