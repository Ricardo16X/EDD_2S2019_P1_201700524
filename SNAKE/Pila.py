import os
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
        temporal = self.ancla
        archivo = open("scoreReport.dot","w")
        archivo.write("digraph G{\n")
        archivo.write("rankdir = \"TB\"\n")
        archivo.write("node [shape = record];\n")
        cadenaResultado = "n1 [shape=record, label=\"{"
        while temporal.siguiente is not None:
            temporal = temporal.siguiente
            cadenaResultado = cadenaResultado + "|(" + str(temporal.coordenadaX) + "," + str(temporal.coordenadaY) + ")"
        cadenaResultado = cadenaResultado + "}\"];"
        archivo.write(cadenaResultado)
        archivo.write("\n}")
        archivo.close()
        os.system("dot -Tjpg scoreReport.dot -o score_report.jpg")
        os.system("score_report.jpg")