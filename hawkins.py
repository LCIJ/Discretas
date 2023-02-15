import sys
import numpy as np


class Node:  # Implementa el objeto Nodo
    def __init__(self, name):
        self.name = name
        self.hijos = []
        self.padres = []

    def addChild(self, nodo):  # Añade un hijo a un nodo, y padres al nodo añadido
        self.hijos.append(nodo)
        for i in nodo.hijos:
            self.hijos.append(i)
        nodo.padres.append(self)


class Graph:  # Implementa objeto Grafo
    def __init__(self):
        self.nodos = []
        self.distances = []
        self.total = 0

    def addNodes(self, nodo):  # Añade un nodo al grafo
        self.nodos.append(nodo)

    def setDistances(self, matrix):  # Le otorga una matriz de adyacencia al grafo
        self.distances = matrix

    def setTotal(self, total):  # Ftorga un costo total al grafo
        self.total = total


def genGraph(arch):  # Función que genera un grafo
    file = open(arch, "r")  # Abrimos el archivo
    storage = {}
    i = 0
    for line in file:  # Exploramos el archivo por línea
        start = line.split(" ")[0]  # Separamos los nombres de los lugares
        fin = line.split(" ")[1]

        if start not in storage.keys():  # Los guardamos como key en el diccionario con un número si es que no estan
            newkey = {start: i}
            storage.update(newkey)
            i += 1
        if fin not in storage.keys():
            newkey = {fin: i}
            storage.update(newkey)
            i += 1
    file.seek(0)  # Devolvemos el cursor al inicio del archivo

    lista = np.zeros((i, i))
    matrix = np.asmatrix(lista)

    for line in file:  # Recorremos de nuevo el archivo
        parts = line.split(" ")
        ini = parts[0]
        fin = parts[1]
        peso = parts[2]
        # Y creamos la matriz de adyacencia con usando los nombres y valores
        matrix[storage[ini], storage[fin]] = int(peso)

    graph = Graph()
    for key in storage.keys():  # Se guardan nodos con los nombres de los lugares en el grafo
        node = Node(key)
        graph.addNodes(node)

    graph.setDistances(matrix)  # Se otroga la matriz de adyacencia al grafo

    return graph


def inChildren(nodo1, nodo2):  # Determina si un nodo está ente los hijos de otro recursivamente
    ans = False
    if nodo1 == [] or nodo2 == []:  # Casos base
        return False
    if nodo1 == nodo2:
        return True

    else:
        for nodo in nodo1.hijos:  # Recursión
            ans = ans or inChildren(nodo, nodo2)
        for nodo in nodo2.hijos:
            ans = ans or inChildren(nodo1, nodo)
    return ans


def inParents(nodo1, nodo2):  # Determina si dos nodos comparten padres recursivamente
    ans = False
    if nodo1.padres == [] or nodo2.padres == []:  # Recursa a los hijos si se llega al tope del arbol
        return inChildren(nodo1, nodo2)
    if nodo2 in nodo1.padres:  # Casos base
        return True
    if nodo1 in nodo2.padres:
        return True
    else:
        for nodo in nodo1.padres:
            ans = ans or inParents(nodo, nodo2)  # Recursión
        for nodo in nodo2.padres:
            ans = ans or inParents(nodo1, nodo)
    return ans


# Busca el valor mínimo en una matriz y devuelve el par ordenado en el que se encuentra.
def min_matrix(graph):
    # Solo devuelve un valor si los nodos no generan loops.
    adj = graph.distances
    min_val = sys.maxsize
    min_side = []
    for i in range(len(adj)):

        for j in range(len(adj)):
            a = (0 < adj[i, j])
            b = (adj[i, j] <= min_val)
            k = graph.nodos[i]
            # Comprueba si comparten padres
            c = not inParents(k, graph.nodos[j])

            if a and b and c:  # Solo copia si no comparten padres
                min_val = adj[i, j]
                min_side = (i, j)
            else:
                continue

    return min_side


def toName(Node):  # Devuelve el nombre de un nodo
    return Node.name


# Devuelve una lista de pares ordenados con los nombres de los lugares.
def showMap(matrix, names):
    mapAns = []
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i, j] != 0:
                mapAns.append((names[i], names[j]))
    return mapAns


# Lo mismo que showMap pero recibe una lista de pares ordenados numéricos y devuelve una de nombres.
def showMapped(pairs, names):
    mapAns = []
    for i in pairs:
        mapAns.append((names[i[0]], names[i[1]]))
    return mapAns


def kruskal(graph):  # Implementa el algoritmo de Kruskal para buscar un árbol de costo mínimos
    adj = graph.distances
    nodes = graph.nodos
    result_matrix = np.zeros((len(adj), len(adj)))
    result_matrix = np.asmatrix(result_matrix)
    largo = 0
    pairs = []
    for i in (range(len(nodes)-1)):  # Itera una vez por arista (nodos-1)

        min = min_matrix(graph)
        # Busca el mínimo de la lista y lo añade (sin loops por min_matrix)
        result_matrix[min[0], min[1]] = adj[min[0], min[1]]

        # Añade parentesco de manera arbitraria
        nodes[min[0]].addChild(nodes[min[1]])
        largo += adj[min[0], min[1]]  # Actualiza el costo
        # Quita el valor de la matriz para ignorarlo la próxima iteración
        adj[min[0], min[1]] = 0
        # Añade el par ordenado a la lista de pares para procesamiento posterior
        pairs.append(min)
    graph.setTotal(largo)  # Le otorga el largo total al grafo

    return (result_matrix, largo, pairs)


if __name__ == "__main__":
    if len(sys.argv) == 1:  # Si se ingresa sin argumentos, se devuelven instrucciones de uso
        print("Ingrese como argumento directorio del archivo que se desea analizar.\n")
        exit()
    graph = genGraph(sys.argv[1])
    # Se genera el grafo y se extraen los nombres de los lugares
    names = list(map(toName, graph.nodos))
    krusk = kruskal(graph)  # Se aplica kruskal
    map1 = showMapped(krusk[2], names)
    print("Matriz de adyacencia del árbol de costo mínimo:\n",
          krusk[0], "\nCoste:", krusk[1], "\nY los lugares que se unen:\n")
    for i in map1:  # Se printean los resultados
        print(i)
    exit()
