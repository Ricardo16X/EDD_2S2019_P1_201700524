import os
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
        # Eliminaré el último
        if self.cantidad > 3:
            self.cantidad -= 1
            self.ultimo = self.ultimo.anterior
            self.ultimo.siguiente = None
            
    
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
    
    def colision(self, comida):
        # esto me regresa a los datos de la cabeza
        temporal = self.ancla.siguiente
        cabezaX = temporal.cX
        cabezaY = temporal.cY
        while temporal.siguiente is not None and comida is True:
            temporal = temporal.siguiente
            if cabezaX == temporal.cX and cabezaY == temporal.cY:
                print("Colisión en : X {0} Y {1}".format(temporal.cX,temporal.cY))
                return True
        return False

    def vaciarSerpiente(self):
        self.ancla.siguiente = None
    
    def generarReporte(self):
        temporal = self.ancla
        nuevoArchivo = open("reporteSnake.dot","w")
        nuevoArchivo.write("digraph G{\n")
        nuevoArchivo.write("rankdir = \"LR\"\n")
        nuevoArchivo.write("node [shape = record];\n")
        cadena = ""
        nuevoArchivo.write("nodoI [shape = record, label=\"null\"];\n")
        nuevoArchivo.write("nodoF [shape = record, label=\"null\"];\n")
        # Creación de los nodos####################
        n = 1
        while temporal.siguiente is not None:
            nodo = "n" + str(n)
            temporal = temporal.siguiente
            cadena = cadena + nodo + " [shape=record, label=\"{|("+ str(temporal.cX) + "," + str(temporal.cY) +")|}\"];\n"
            nuevoArchivo.write(nodo + " [shape=record, label=\"{|("+ str(temporal.cX) + "," + str(temporal.cY) +")|}\"];\n")
            n = n + 1
        ############################################
        i = 1
        n = n - 1
        # Uso de los nodos
        # Nodo primero
        nuevoArchivo.write("nodoI -> n1 [dir=\"back\"];")
        while i < n:
            cadena = cadena + "n" + str(i) + " -> " + "n"+str(i+1)+"\n"
            nuevoArchivo.write("n" + str(i) + " -> " + "n"+str(i+1)+"\n")
            cadena = cadena + "n" + str(i+1) + " -> " + "n"+str(i)+"\n"
            nuevoArchivo.write("n" + str(i+1) + " -> " + "n"+str(i)+"\n")
            i = i + 1
        #Nodo ultimo
        nuevoArchivo.write("n" + str(n) + " -> nodoF [dir=\"forward\"];")
        print(cadena)
        nuevoArchivo.write("}")
        nuevoArchivo.close()
        os.system("dot -Tjpg reporteSnake.dot -o reporteSnake.jpg")
        os.system("reporteSnake.jpg")