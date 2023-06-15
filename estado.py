class Estado():

    # Metodo constructor de la clase
    # Cada estado tendra los 4 caballos, un rey, el estado padre, la profundidad en el grafo, el valor heuristico y un nombre
    def __init__(self, r, c1, c2, c3, c4, padre, profundidad, valor_heuristico, nombre):
        self.r = r
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3
        self.c4 = c4
        self.padre = padre
        self.profundidad = profundidad
        self.valor_heuristico = valor_heuristico
        self.nombre = nombre
        self.adyacentes = self.r.casillas_adyacentes()
        self.adyacentes = [(x, y, False) for x, y in self.adyacentes]

    def validar_estado_objetivo(self):
        for adyacente in self.adyacentes:
            if not adyacente[2]:
                return False
        return True


    # Metodo que modifica el como se muestra un objeto en consola
    # Al hacer print de un objeto de esta clase, se mostrara lo que retorne el siguiente metodo
    def __str__(self):
        # La f hace que podamos concatenar variables al string de forma comoda usando las llaves {}
        return f'Nombre: {self.nombre}\nCaballo 1: {self.c1}\nCaballo 2:{self.c2}\nCaballo 3: {self.c3}\nCaballo 4:{self.c4}\nRey: {self.r}\nValorH: {self.valor_heuristico}\nAdyacentes: {self.adyacentes}\n'


    def generar_valor_heuristico(self):
        control_total = 0
        piezas = [self.c1, self.c2, self.c3, self.c4]
        for pieza in piezas:
            movs = pieza.generar_movimientos_caballo(piezas)
            for i, it in enumerate(self.adyacentes):
                for mov in movs:
                    if (mov[0] == it[0] and mov[1] == it[1]) and (it[2] == False):
                        new_tuple = (it[0], it[1], True)
                        self.adyacentes[i] = new_tuple
                        control_total += 20
        for i, it in enumerate(self.adyacentes):
            if (it[0] == self.r.x) and (it[1] == self.r.y) and (it[2]):
                for adyacente in self.adyacentes:
                    if not adyacente[2]:
                        self.valor_heuristico = -10000
                        new_tuple = (it[0], it[1], False)
                        self.adyacentes[i] = new_tuple
                        break
                break

        distancia_total = (
            abs(self.c1.x - self.r.x) +
            abs(self.c1.y - self.r.y) +
            abs(self.c2.x - self.r.x) +
            abs(self.c2.y - self.r.y) +
            abs(self.c3.x - self.r.x) +
            abs(self.c3.y - self.r.y) +
            abs(self.c4.x - self.r.x) +
            abs(self.c4.y - self.r.y)
            )
        self.valor_heuristico += control_total - distancia_total

    def mostrar_tablero(self):
        tablero = [[0 for j in range(8)] for i in range(8)]
        tablero[self.r.x][self.r.y] = 'r'
        tablero[self.c1.x][self.c1.y] = 1
        tablero[self.c2.x][self.c2.y] = 2
        tablero[self.c3.x][self.c3.y] = 3
        tablero[self.c4.x][self.c4.y] = 4
        for fila in tablero:
            for elemento in fila:
                print(elemento, end=' ')
            print()
        print()

    def __eq__(self, other):
        if isinstance(other, Estado):
            return self.r == other.r and \
                   self.c1 == other.c1 and \
                   self.c2 == other.c2 and \
                   self.c3 == other.c3 and \
                   self.c4 == other.c4
        return False



