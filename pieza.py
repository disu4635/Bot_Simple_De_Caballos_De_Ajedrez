class Pieza():
    # Metodo constructor de la clase
    # Cada pieza tiene una posicion en x, en y el tipo de pieza, caballo o rey
    def __init__(self, x, y, tipo):
        self.x = x
        self.y = y
        self.tipo = tipo
    
    # Metodo que modifica el como se muestra un objeto en consola
    # Al hacer print de un objeto de esta clase, se mostrara lo que retorne el siguiente metodo
    def __str__(self):
        # La f hace que podamos concatenar variables al string de forma comoda usando las llaves {}
        return f'[{self.x},{self.y},{self.tipo}]'

    
    def generar_movimientos_caballo(self, piezas):
        movimientos = []
        desplazamientos = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]

        for dx, dy in desplazamientos:
            nueva_x = self.x + dx
            nueva_y = self.y + dy

            # Verificar si la nueva casilla está dentro del tablero y no está ocupada por otra pieza
            if nueva_x >= 0 and nueva_x <= 7 and nueva_y >= 0 and nueva_y <= 7:
                ocupada = False
                for pieza in piezas:
                    if pieza.x == nueva_x and pieza.y == nueva_y:
                        ocupada = True
                        break
                if not ocupada:
                    movimientos.append((nueva_x, nueva_y))

        return movimientos
    

    def casillas_adyacentes(self):
        adyacentes = [(self.x, self.y)]
        if self.x == 0:
            adyacentes.append((self.x+1, self.y))
            if self.y == 0:
                adyacentes.append((self.x+1, self.y+1))
                adyacentes.append((self.x, self.y+1))
            elif self.y == 7:
                adyacentes.append((self.x+1, self.y-1))
                adyacentes.append((self.x, self.y-1))
            else:
                adyacentes.append((self.x, self.y+1))
                adyacentes.append((self.x, self.y-1))
                adyacentes.append((self.x+1, self.y+1))
                adyacentes.append((self.x+1, self.y-1))
        elif self.x == 7:
            adyacentes.append((self.x-1, self.y))
            if self.y == 0:
                adyacentes.append((self.x-1, self.y+1))
                adyacentes.append((self.x, self.y+1))
            elif self.y == 7:
                adyacentes.append((self.x-1, self.y-1))
                adyacentes.append((self.x, self.y-1))
            else:
                adyacentes.append((self.x, self.y+1))
                adyacentes.append((self.x, self.y-1))
                adyacentes.append((self.x-1, self.y+1))
                adyacentes.append((self.x-1, self.y-1))
        elif self.y == 0:
            adyacentes.append((self.x, self.y+1))
            adyacentes.append((self.x+1, self.y))
            adyacentes.append((self.x-1, self.y))
            adyacentes.append((self.x+1, self.y+1))
            adyacentes.append((self.x-1, self.y+1))
        elif self.y == 7:
            adyacentes.append((self.x, self.y-1))
            adyacentes.append((self.x+1, self.y))
            adyacentes.append((self.x-1, self.y))
            adyacentes.append((self.x+1, self.y-1))
            adyacentes.append((self.x-1, self.y-1))

        # retornar la lista de casillas adyacentes
        return adyacentes

    def __eq__(self, other):
        if isinstance(other, Pieza):
            return self.x == other.x and self.y == other.y
        return False