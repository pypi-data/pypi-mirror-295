from colorama import Fore
import os

def clear():
    os.system('cls' if os.name=='nt' else 'clear')

class Color:
    WHITE = Fore.WHITE
    BLUE = Fore.BLUE
    RED = Fore.RED


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class Tile:
    def __init__(self):
        self.char = '█'
        self.color = Color.WHITE

class Player(Tile):
    def __init__(self):
        self.color = Color.BLUE
        self.position = Point(0, 0)
        
        super().__init__()

class Game:

    def __init__(self):
        self.__grid__ = {}
        self.__hud__ = []
        self.width = 100
        self.height = 100
        self.PLAYER = Player()
        self.view_distance = 9
        self.__error_message__ = ""

    def setup(self):
        for x in range(self.width):
            for y in range(self.height):
                self.__grid__[(x, y)] = Tile()
        
        self.draw()

    def add_hud_element(self, key: str, desc: str, function):
        self.__hud__.append({"key": key, "desc": desc, "function": function})
        

    def draw_hud(self):
        print(Color.RED + self.__error_message__ + Color.WHITE)
        for hud_element in self.__hud__:
            print(f"{hud_element['key']} - {hud_element['desc']}")

    def check_input(self):
        inp = input(Color.WHITE + ">>> ")
        self.__error_message__ = ""

        for hud_element in self.__hud__:
            if inp == hud_element['key']:
                hud_element["function"]()

        

    def draw(self):
        posX = self.PLAYER.position.x
        posY = self.PLAYER.position.y
        self.__grid__[(posX, posY)] = self.PLAYER
        for y in range(posY, self.view_distance + posY):
            string = ""
            for x in range(posX, self.view_distance + posX):
                obj = self.__grid__[(x, y)]
                string += obj.color + obj.char + " "
            
            print(string)
        
        self.draw_hud()
        self.check_input()
        clear()
        self.draw()

                
                
