class nodoPila():
    coordenadaX = 0
    coordenadaY = 0
    siguiente = None
    def __init__(self, coordX, coordY):
        self.coordenadaX = coordX
        self.coordenadaY = coordY
        self.siguiente = None

class Pila():
    ancla = None
    def __init__(self):
        self.ancla = nodoPila(None, None)
        self.ancla.siguiente = None
    
    def push(self, coordX, coordY):
        temporal = self.ancla
        nueva_Coordenada = nodoPila(coordX,coordY)
        if temporal.siguiente is None:
            temporal.siguiente = nueva_Coordenada
        else:
            primero = temporal.siguiente
            temporal.siguiente = nueva_Coordenada
            nueva_Coordenada.siguiente = primero
            
    def vaciar(self):
        self.ancla.siguiente = None
        
    def graficar(self):
        #M�todo para graficar y generar el reporte xd
        temporal = self.ancla