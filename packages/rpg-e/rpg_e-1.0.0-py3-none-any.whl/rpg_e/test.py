from game import Game, Color

game = Game()

game.PLAYER.color = Color.BLUE

def hello():
    game.__error_message__ = "Hello"

game.add_hud_element("r", "Hello", hello)

game.setup()


