class nodoDE():
    def __init__(self, coordY, coordX):
        self.cX = coordX
        self.cY = coordY
        self.siguiente = None
        self.anterior = None
        self.char = '#'

class listaDE():
    def __init__(self):
        self.ancla = nodoDE(None,None)
        self.ultimo = None
        self.primero = None
        self.cantidad = 0
    
    def insertar(self,coordY,coordX):
        temporal = self.ancla
        nuevoNodoLista = nodoDE(coordY,coordX)
        self.cantidad += 1
        if temporal.siguiente is None:
            self.ancla.siguiente = nuevoNodoLista
            self.ultimo = nuevoNodoLista
        else:
            #Se implementará siempre insertar de último
            tempUltimo = self.ultimo
            self.ultimo.siguiente = nuevoNodoLista
            nuevoNodoLista.anterior = tempUltimo
            self.ultimo = nuevoNodoLista
    
    def eliminar(self):
        temporal = self.ancla
        if self.cantidad > 3:
            self.cantidad -= 1
            primero = temporal.siguiente
            temporal.siguiente = primero.siguiente
            primero.siguiente = None
    
    def actualizar(self, CX, CY):
        temporal = self.ancla.siguiente
        MI_X = CX
        MI_Y = CY
        MD_X = 0
        MD_Y = 0
        while temporal.siguiente is not None:
            temporal = temporal.siguiente
            MD_X = temporal.cX
            MD_Y = temporal.cY
            temporal.cX = MI_X
            temporal.cY = MI_Y
            MI_X = MD_X
            MI_Y = MD_Y
