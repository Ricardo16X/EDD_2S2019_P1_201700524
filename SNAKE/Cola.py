#SCOREBOARD DE USUARIOS
class nodoCola():
    siguiente = None
    def __init__(self, nombre, punteo):
        # Elementos para la "identificación de los Nodos"
        self.nombre = nombre
        self.puntuacion = punteo
        self.siguiente = None

class Cola():
    ancla = None
    ultimo = None
    numeroPunteos = 0
    def __init__(self):
        self.ancla = nodoCola(None, None)
        self.ultimo = None
    
    def push(self,nombre,punteo):
        temporal = self.ancla
        #Verifico si el ancla no apunta a nada
        if temporal.siguiente is None:
            # Creo el nodo para la nueva puntuación
            # El nuevo puntero apuntará a nulo
            nuevo_enCola = nodoCola(nombre,punteo)
            # Agrego el Ultimo a la Cola
            ## El puntero ultimo apuntará hacia el nuevo item agregado
            self.ultimo = nuevo_enCola
            # Ahora el ancla apunta hacia el nuevo item agregado
            temporal.siguiente = nuevo_enCola
            self.numeroPunteos = 1
        else:
            ## OK el temporal apunta hacia algo distinto de null
            # entonces empezaré a crear un nuevo nodo en la cola
            # y lo insertaré de ultimo
            if self.numeroPunteos <= 10:
                nuevo_enCola = nodoCola(nombre, punteo)
                self.numeroPunteos += 1
                #OK ya creado el nuevo puntero busco el ultimo
                self.ultimo.siguiente = nuevo_enCola
                ##Borro la referencia anterior de ultimo. Ya que se ha creado un nuevo nodo
                self.ultimo = None
                self.ultimo = nuevo_enCola
            else:
                nuevo_enCola = nodoCola(nombre, punteo)
                self.numeroPunteos += 1
                #OK ya creado el nuevo puntero busco el ultimo
                self.ultimo.siguiente = nuevo_enCola
                ##Borro la referencia anterior de ultimo. Ya que se ha creado un nuevo nodo
                self.ultimo = None
                self.ultimo = nuevo_enCola
                #Saco al primero de la cola en caso de haber llegado a 10
                self.pop()

    def pop(self):
        temporal = self.ancla
        if temporal.siguiente is None:
            return "Sin punteos actualmente"
        else:
            primero_enCola = temporal.siguiente
            temporal.siguiente = primero_enCola.siguiente
            primero_enCola.siguiente = None

    def graficar(self):
        temporal = self.ancla
        ## Instrucciones para la graficación