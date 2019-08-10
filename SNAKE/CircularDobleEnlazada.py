#reporte de usuarios registrados en el juego
class nodoCDEnlazada():
    def __init__(self,nombre):
        self.nombre = nombre
        self.siguiente = None
        self.anterior = None
        
class CDEnlazada():
    def __init__(self):
        self.ancla = nodoCDEnlazada(None)
        self.ultimo = None
        self.primero = None
        
    def ingresar(self, nombreUsuario):
        temporal = self.ancla
        #Creaci�n de nuevo nodo
        nuevoRegistroUsuario = nodoCDEnlazada(nombreUsuario)
        if temporal.siguiente is None:
            # Es el primer elemento de la lista circular doble
            temporal.siguiente = nuevoRegistroUsuario
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