import sys
import numpy as np
from hawkins import genGraph, kruskal, Graph, Node, toName, showMap


def genTree(arch):  # Genera un arbol a partir de un archivo
    # Primero creamos la matriz para generar el arbol
    graphed = genGraph(arch)  # Se llama a genGraph para generar el grafo
    krusk = kruskal(graphed)
    matrix = krusk[0]
    total = krusk[1]
    # Luego generamos el arbol a partir de la matriz
    resultGraph = Graph()

    for i in range(len(matrix)):  # Generamos un nuevo set de nodos
        nnode = Node(i)
        resultGraph.addNodes(nnode)

    for i in resultGraph.nodos:  # Y les damos parentesco
        for j in resultGraph.nodos:
            if matrix[i.name, j.name] != 0:
                i.addChild(j)

    names = list(map(toName, graphed.nodos))  # Luego extraemos los nombres
    resultGraph.setDistances(matrix)  # Otorgamos la matriz
    resultGraph.setTotal(total)  # Y el total
    return resultGraph, names


def getMax(matrix):  # Obtiene el máximo de una matriz
    max_val = 0
    obj = (0, 0)
    for j in range(len(matrix)):
        for k in range(len(matrix)):
            a = (0 < matrix[j, k])
            b = (matrix[j, k] >= max_val)
            if a and b:
                max_val = matrix[j, k]
                obj = (j, k)

    return obj


def findIdeal(matrix, diff):  # Obtiene el valor ideal a restar de un grafo dada una limitante
    closer = diff
    target = (0, 0)
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i, j] != 0:
                close = diff-matrix[i, j]
                if abs(close) < closer:  # Busca cual es el valor que acerca más la diferencia a 0
                    closer = close
                    target = (i, j)

    if closer <= 0:  # Si al final la diferencia es 0 o negativa devuelve este valor
        return target
    else:  # Si no, retorna el valor máximo
        return getMax(matrix)


def limit_forest(tree, n):  # Entrega una matriz de adyacencia que resuelve la limitante creando un bosque, y la diferencia final
    matrix = tree.distances
    total = tree.total
    diff = total-n
    while diff > 0:  # Itera mientras la diferencia entre el coste y la limitante sea mayor a cero
        # Llama a findIdeal para buscar la mejor opción a eliminar
        elim = findIdeal(matrix, diff)
        diff -= matrix[elim[0], elim[1]]  # Resta el valor de la diferencia

        matrix[elim[0], elim[1]] = 0  # Y luego la elimina de la matriz
    return matrix, diff


def findHojas(matrix):  # Algoritmo que busca hojas en un arbol
    count = [0]*len(matrix)
    ans = []
    for i in range(len(matrix)):
        # Cuenta la cantidad de ocurrencias de cada nodo en la matriz
        for j in range(len(matrix)):
            if matrix[i, j] != 0:
                count[i] += 1
                count[j] += 1

    for i in range(len(count)):
        if count[i] == 1:  # Si el nodo ocurre solo una vez, es hoja
            ans.append(i)

    return ans  # Devuelve la lista de hojas


# Devuelve una matriz de adyacencia que resuelve la limitante creando un solo arbol, y la diferencia final.
def limit_tree(tree, n):
    nodes = tree.nodos
    matrix = tree.distances
    total = tree.total
    diff = total-n

    while diff > 0:  # Itera mientras la diferencia sea mayor a cero
        # Define que valores serán revisados llamando a findHojas
        recorrido = findHojas(matrix)
        ansplate = np.zeros((len(nodes), len(nodes)))
        ansMat = np.asmatrix(ansplate)
        for i in recorrido:
            i = int(i)
            # Recorre limitándose a las hojas, generando una matriz que findIdeal pueda aceptar
            for j in range(len(nodes)):
                if matrix[i, j] != 0:
                    ansMat[i, j] = matrix[i, j]
                if matrix[j, i] != 0:
                    ansMat[j, i] = matrix[j, i]

        elim = findIdeal(ansMat, diff)  # Llama a findIdeal con la matriz nueva
        diff -= matrix[elim[0], elim[1]]
        # Y elimina de la matriz original el valor
        matrix[elim[0], elim[1]] = 0
    return matrix, diff


if __name__ == "__main__":
    if len(sys.argv) == 1:  # Si no hay argumentos printea instrucciones
        print("Ingrese como argumento directorio del archivo que se desea analizar seguido de el límite de metros de cañerías a usar.\n")
        exit()
    if len(sys.argv) == 2:  # Si no incluye limitante, avisa al respecto
        print("Debe ingresar un límite de metros.\n")
        exit()
    if int(sys.argv[2]) < 0:  # Si la limitante es negativa, también avisa
        print("Por favor ingrese un límite mayor o igual a 0")
        exit()

    tree = genTree(sys.argv[1])[0]  # Generamos dos árboles distintos
    tree2 = genTree(sys.argv[1])[0]
    names = genTree(sys.argv[1])[1]

    # Aplicamos las limitantes
    forestAns = limit_forest(tree, int(sys.argv[2]))
    treeAns = limit_tree(tree2, int(sys.argv[2]))

    # Llamamos a las funciones que devuelven pares ordenados
    map1 = showMap(forestAns[0], names)
    map2 = showMap(treeAns[0], names)

    print("Matriz de adyacencia que genera un bosque:\n",
          forestAns[0])  # Printeamos los resultados
    print("\nLos pares de lugares que se unen:\n")
    for i in map1:
        print(i, " ")
    print("\nY que tan cerca de los requerimientos está:", -
          forestAns[1], "metros bajo el requerimiento\n")
    print("Matriz de adyacencia que genera un arbol:\n", treeAns[0])
    print("\nLos pares de lugares que se unen:\n")
    for i in map2:
        print(i, " ")
    print("\nY que tan cerca de los requerimientos está:", -
          treeAns[1], "metros bajo el requerimiento\n")
