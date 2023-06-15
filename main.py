from enum import Enum
from typing import Optional
import numpy as np
import pygame as pg
from pygame import Surface
from core.game import Game
from core.gameObject import GameObject
from core.scene import Scene
from pieza import Pieza
from estado import Estado
import copy

def generar_hijos(estado: Estado, cerrados):
    hijos = []
    caballos = [estado.c1, estado.c2, estado.c3, estado.c4]
    for caballo in caballos:
        movs = caballo.generar_movimientos_caballo(caballos)
        for mov in movs:
            if mov[0] == estado.r.x and mov[1] == estado.r.y:
                continue
            nuevo_estado = Estado(copy.deepcopy(estado.r), copy.deepcopy(estado.c1), copy.deepcopy(estado.c2), copy.deepcopy(estado.c3), copy.deepcopy(estado.c4), estado, estado.profundidad + 1, 0, 0)

            # Actualizar la coordenada del caballo actual con el movimiento generado
            if caballo == estado.c1:
                nuevo_estado.c1.x = mov[0]
                nuevo_estado.c1.y = mov[1]
            elif caballo == estado.c2:
                nuevo_estado.c2.x = mov[0]
                nuevo_estado.c2.y = mov[1]
            elif caballo == estado.c3:
                nuevo_estado.c3.x = mov[0]
                nuevo_estado.c3.y = mov[1]
            elif caballo == estado.c4:
                nuevo_estado.c4.x = mov[0]
                nuevo_estado.c4.y = mov[1]

            explorado = False
            
            for cerrado in cerrados:
                if cerrado == nuevo_estado:
                    explorado = True
                    break
            
            if explorado: continue

            nuevo_estado.generar_valor_heuristico()
            # Agregar el nuevo estado a la lista de hijos
            hijos.append(nuevo_estado)
    
    return hijos  
    
# Generar casillas adyacentes

def definir_camino(estado: Estado, camino):
    camino.append(estado)
    if estado.padre:
        definir_camino(estado.padre, camino)
    return camino   

SCREEN_SIZE = 600
TILE_SIZE = int(SCREEN_SIZE / 8)
COLS = ["A", "B", "C", "D", "E", "F", "G", "H"]


class Colors:
    BG_LIGHT = (238, 238, 210)
    BG_DARK = (118, 150, 86)


class Teams(Enum):
    WHITE = 0
    BLACK = 1


class PieceType(Enum):
    PAWN = 0
    ROOK = 1
    KNIGHT = 2
    BISHOP = 3
    QUEEN = 4
    KING = 5


class Piece(GameObject):
    def __init__(
        self, image: str, _type: PieceType, team: Teams, position: tuple[int, int]
    ):
        super().__init__()
        self.team = team
        self.type = _type
        self.alive = True
        self.image = pg.image.load(image)
        self.marginx = int((TILE_SIZE - self.image.get_size()[0]) / 2)
        self.marginy = int((TILE_SIZE - self.image.get_size()[1]) / 2)
        self.position = position

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, new_pos: tuple[int, int]):
        self._position = new_pos
        self.transform.setPosition((new_pos[1]) * TILE_SIZE + self.marginy, new_pos[0] * TILE_SIZE + self.marginx)

    def move(self, row: int,  col: int):
        self.position = (row, col)

    def draw(self, surface: Surface):
        if self.alive:
            self.image.get_size()
            surface.blit(
                self.image,
                (
                    self.transform.x,
                    self.transform.y,
                ),
            )


class Tile(GameObject):
    def __init__(self, x, y, row, col, color):
        super().__init__()
        self.transform.setPosition(x, y)
        self.color = color
        self.row = row
        self.col = col

    @property
    def rect(self):
        return (self.transform.x, self.transform.y, TILE_SIZE, TILE_SIZE)

    def draw(self, surface: Surface):
        pg.draw.rect(surface, self.color, self.rect)
        my_font = pg.font.SysFont("Comic Sans MS", 30)
        text_surface = my_font.render(f"{self.row}{self.col}", False, (0, 0, 0))
        surface.blit(text_surface, self.rect)


class Chessboard(GameObject):
    def __init__(self):
        super(Chessboard, self).__init__()
        self.tiles: list[Tile] = []
        self.pieces: list[Piece] = []
        self.setup_tiles()
        self.setup_pieces()

    def setup_tiles(self):
        col = 0
        colorFlag = True
        self.tiles: list[Tile] = []
        for x in np.linspace(0, SCREEN_SIZE, 9)[:-1]:
            row = 0
            for y in np.linspace(0, SCREEN_SIZE, 9)[:-1]:
                color = Colors.BG_LIGHT if colorFlag else Colors.BG_DARK
                self.tiles.append(Tile(x, y, row, col, color))
                colorFlag = not colorFlag
                row += 1
            colorFlag = not colorFlag
            col += 1

    def setup_pieces(self):
        self.knight1 = Piece(
            "./pieces/KnightWhite.png", PieceType.KNIGHT, Teams.WHITE, (0, 1)
        )
        self.knight2 = Piece(
            "./pieces/KnightWhite.png", PieceType.KNIGHT, Teams.WHITE, (0, 2)
        )
        self.knight3 = Piece(
            "./pieces/KnightWhite.png", PieceType.KNIGHT, Teams.WHITE, (0, 3)
        )
        self.knight4 = Piece(
            "./pieces/KnightWhite.png", PieceType.KNIGHT, Teams.WHITE, (0, 4)
        )
        self.king = Piece("./pieces/KingBlack.png", PieceType.KING, Teams.BLACK, (7, 7))
        self.pieces = [
            self.knight1,
            self.knight2,
            self.knight3,
            self.knight4,
            self.king,
        ]

    def draw(self, surface: Surface):
        for tile in self.tiles:
            tile.draw(surface)
        for piece in self.pieces:
            piece.draw(surface)


class ChessScene(Scene):
    def initGameObjects(self):
        self.gameObjects["Chessboard"] = Chessboard()
        # todo calculate steps
        cerrados = []  # Lista de cerrados

        # Creacion de objetos de tipo pieza para pruebas
        c1 = Pieza(0, 1, 'C1')
        c2 = Pieza(0, 2, 'C2')
        c3 = Pieza(0, 3, 'C3')
        c4 = Pieza(0, 4, 'C4')
        r = Pieza(7, 7, 'R')

        # Creacion de un estado para pruebas
        Ei = Estado(r, c1, c2, c3, c4, None, 1, 0, 'EI')
        abiertos = [Ei]  # Lista de abiertos
        Ea = None
        exito = False
        Eo = None
        camino=[]

        Ei.generar_valor_heuristico()

        while not exito and len(abiertos) != 0:
            Ea = abiertos.pop(0)
            if Ea.validar_estado_objetivo(): 
                Exito = True
                Eo = copy.deepcopy(Ea)
                break
            hijos = generar_hijos(Ea, cerrados)
            
            # Definir una función lambda para obtener el valor_heuristico de un estado
            obtener_valor_heuristico = lambda estado: estado.valor_heuristico
            # Ordenar la lista hijos de mayor a menor por el atributo valor_heuristico
            abiertos.extend(hijos)
            abiertos = sorted(abiertos, key=obtener_valor_heuristico, reverse=True)
            cerrados.append(Ea)
            Ea = None

        self.steps = []

        # for i in cerrados:
        #     print(i.mostrar_tablero(), i.valor_heuristico)

        # for i in abiertos:
        #     print(i.mostrar_tablero(), i.valor_heuristico)

        # print(len(abiertos))
        # print(len(cerrados))

        if Exito:
            camino = []
            camino = definir_camino(Eo, camino)
            camino.reverse()
            for paso in camino:
                self.steps.append({
                    "knight1": (paso.c1.x, paso.c1.y),
                    "knight2": (paso.c2.x, paso.c2.y),
                    "knight3": (paso.c3.x, paso.c3.y),
                    "knight4": (paso.c4.x, paso.c4.y),
                })
            paso.mostrar_tablero()

        # self.steps = [
        #     {
                # "knight1": (1, 1),
                # "knight2": (2, 1),
                # "knight3": (3, 1),
                # "knight4": (4, 1),
        #     },
        #     {
        #         "knight1": (2, 2),
        #         "knight2": (3, 2),
        #         "knight3": (4, 2),
        #         "knight4": (5, 2),
        #     },
        #     {
        #         "knight1": (3, 3),
        #         "knight2": (4, 3),
        #         "knight3": (5, 3),
        #         "knight4": (6, 3),
        #     },
        # ]
        self.currentStep = 0

    def update(self, events, keys):
        for event in events:
            if (
                event.type == pg.MOUSEBUTTONDOWN
                and event.button == 1
                and self.currentStep < len(self.steps)
            ):
                chessboard = self.getGameObject("Chessboard")
                for key, value in self.steps[self.currentStep].items():
                    getattr(chessboard, key).move(*value)
                self.currentStep += 1


if __name__ == "__main__":
    Game(SCREEN_SIZE, SCREEN_SIZE, title="Chess").setupScenes([ChessScene]).run()
