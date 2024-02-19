import arcade
from enum import Enum
import math
from random import sample

TOTAL_MINE = 40
SCREEN_TITLE = "Mine Sweeper"
# good numbers colums X rows 20 X 15 bombs 30
GRID_COLUMNS = 20
GRID_ROWS = 15
SPRITE_SHEET_PATH = "./sprites.png"
SPRITE_NATIVE_SIZE = 16
SPRITE_SCALE = 4
SPRITE_FINAL_SIZE = SPRITE_SCALE * SPRITE_NATIVE_SIZE
SPRITE_HALF_SIZE = SPRITE_FINAL_SIZE / 2
SCREEN_WIDTH = GRID_COLUMNS * SPRITE_FINAL_SIZE
SCREEN_HEIGHT = GRID_ROWS * SPRITE_FINAL_SIZE


class SquareImage(Enum):
    BLANK_UP = 1
    BLANK_DOWN = 2
    FLAG = 3
    QUESTION_UP = 4
    QUESTION_DOWN = 5
    MINE_GREY = 6
    MINE_RED = 7
    MINE_X = 8
    ONE = 9
    TWO = 10
    THREE = 11
    FOUR = 12
    FIVE = 13
    SIX = 14
    SEVEN = 15
    EIGHT = 16


class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y


SHEET_OFFSETS = {
    SquareImage.BLANK_UP: Coordinate(0, 50),
    SquareImage.BLANK_DOWN: Coordinate(16, 50),
    SquareImage.FLAG: Coordinate(33, 50),
    SquareImage.QUESTION_UP: Coordinate(50, 50),
    SquareImage.QUESTION_DOWN: Coordinate(67, 50),
    SquareImage.MINE_GREY: Coordinate(84, 50),
    SquareImage.MINE_RED: Coordinate(101, 50),
    SquareImage.MINE_X: Coordinate(118, 50),
    SquareImage.ONE: Coordinate(0, 68),
    SquareImage.TWO: Coordinate(16, 68),
    SquareImage.THREE: Coordinate(33, 68),
    SquareImage.FOUR: Coordinate(50, 68),
    SquareImage.FIVE: Coordinate(67, 68),
    SquareImage.SIX: Coordinate(84, 68),
    SquareImage.SEVEN: Coordinate(101, 68),
    SquareImage.EIGHT: Coordinate(118, 68),
}


class Square:
    def __init__(self, x, y, i, j):
        offset = SHEET_OFFSETS[SquareImage.BLANK_UP]
        self.image = SquareImage.BLANK_UP
        self.sprite = arcade.Sprite(
            SPRITE_SHEET_PATH,
            SPRITE_SCALE,
            offset.x,
            offset.y,
            SPRITE_NATIVE_SIZE,
            SPRITE_NATIVE_SIZE,
        )
        self.x = x
        self.y = y
        self.sprite.center_x = x
        self.sprite.center_y = y
        self.i = i
        self.j = j

        self.is_bomb = False
        self.is_flag = False
        self.adjacent_bomb_count = 0

    def draw_as(self, image):
        offset = SHEET_OFFSETS[image]
        self.sprite = arcade.Sprite(
            SPRITE_SHEET_PATH,
            SPRITE_SCALE,
            offset.x,
            offset.y,
            SPRITE_NATIVE_SIZE,
            SPRITE_NATIVE_SIZE,
        )
        self.sprite.center_x = self.x
        self.sprite.center_y = self.y
        self.image = image 

    def draw(self):
        self.sprite.draw()


class MinesweeperGame(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.WHITE)
        self.squares = []
        for i in range(GRID_COLUMNS):
            x = i * SPRITE_FINAL_SIZE + SPRITE_HALF_SIZE
            for j in range(GRID_ROWS):
                y = j * SPRITE_FINAL_SIZE + SPRITE_HALF_SIZE
                self.squares.append(Square(x, y, i, j))
        self.place_mines()

    def place_mines(self):
        posible_bomb = sample(self.squares, TOTAL_MINE)
        for bomb in posible_bomb:
            bomb.is_bomb = True
            # for debugging uncomment
            bomb.draw_as(SquareImage.MINE_GREY)

        self.count_adjacnent_mine(posible_bomb)

    def draw_adjacent_bomb_count(self, square):
        if square.adjacent_bomb_count == 1:
            square.draw_as(SquareImage.ONE)
        if square.adjacent_bomb_count == 2:
            square.draw_as(SquareImage.TWO)
        if square.adjacent_bomb_count == 3:
            square.draw_as(SquareImage.THREE)
        if square.adjacent_bomb_count == 4:
            square.draw_as(SquareImage.FOUR)
        if square.adjacent_bomb_count == 5:
            square.draw_as(SquareImage.FIVE)
        if square.adjacent_bomb_count == 6:
            square.draw_as(SquareImage.SIX)
        if square.adjacent_bomb_count == 7:
            square.draw_as(SquareImage.SEVEN)
        if square.adjacent_bomb_count == 8:
            square.draw_as(SquareImage.EIGHT)

    def count_adjacnent_mine(self, bombs):
        # for every square set adjacent_bomb_count to the correct number
        # argument bombs is all the squares that are bombs
        # every square has index i and j to identify where it is
        for bomb in bombs:
            for i_offset in range(-1, 2):
                i = bomb.i + i_offset
                if i < 0 or i >= GRID_COLUMNS:
                    continue
                for j_offset in range(-1, 2):
                    j = bomb.j + j_offset
                    if j < 0 or j >= GRID_ROWS:
                        continue

                    index = self.get_mine_index_ij(i, j)
                    adjacent_square = self.squares[index]
                    if not adjacent_square.is_bomb:
                        adjacent_square.adjacent_bomb_count = (
                            adjacent_square.adjacent_bomb_count + 1
                        )
                        # for debugging uncomment
                        #self.draw_adjacent_bomb_count(adjacent_square)

    def get_mine_index_ij(self, i, j):
        return i * GRID_ROWS + j

    def get_mine_index_xy(self, x, y):
        i = math.floor(x / SPRITE_FINAL_SIZE)
        j = math.floor(y / SPRITE_FINAL_SIZE)
        index = self.get_mine_index_ij(i, j)
        # print("i {0}, j {1}, index {2}".format(i, j, index))
        return index

    def on_mouse_press(self, x, y, button, key_modifiers):
        index = self.get_mine_index_xy(x, y)

        if button == arcade.MOUSE_BUTTON_RIGHT:
            if self.squares[index].is_flag:
                self.squares[index].is_flag = False
                self.squares[index].draw_as(SquareImage.BLANK_UP)
            else:
                self.squares[index].is_flag = True
                self.squares[index].draw_as(SquareImage.FLAG)

        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.squares[index].is_bomb:
                print("you lost")
                arcade.close_window()
            elif self.squares[index].adjacent_bomb_count == 0:
                square = self.squares[index]
                two2_prossess = [square] 
                while two2_prossess:
                    square = two2_prossess[0]
                    two2_prossess.remove(square)
                    for i_offset in range(-1, 2):
                        for j_offset in range(-1, 2):
                            squarzx = square.i + i_offset 
                            squarzy = square.j + j_offset
                            if squarzx < 0 or squarzx >= GRID_COLUMNS:
                                continue
                            if squarzy < 0 or squarzy >= GRID_ROWS:
                                continue

                            indexx = self.get_mine_index_ij(squarzx, squarzy)
                            squarezz = self.squares[indexx]
                            if squarezz.adjacent_bomb_count > 0: 
                                self.draw_adjacent_bomb_count(squarezz)    
                                continue
                            if squarezz.image == SquareImage.BLANK_UP: 
                                two2_prossess.append(squarezz)
                            squarezz.draw_as(SquareImage.BLANK_DOWN)
                            #elif self.squares[index].is_bomb:
                            #        squarezz.draw_as(SquareImage.MINE_GREY)
                            #else:
                            #    squarezz.draw_as(SquareImage.BLANK_DOWN)
                            


                            
                                

                                        
                        
                #for square in squares:


    def on_draw(self):
        arcade.start_render()
        for s in self.squares:
            s.draw()


def main():
    _ = MinesweeperGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()


if __name__ == "__main__":
    main()


#self.square.draw_as(SquareImage.BLANK_UP)
