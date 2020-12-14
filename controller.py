"""
# A class to store the application control
"""
import glfw
from sys import exit
import numpy as np

class Controller:
    def __init__(self):
        self.snake = None
        self.camera = None
        self.gameStart = False

    def on_key(self, window, key, scancode, action, mods):

        if not (action == glfw.REPEAT or action == glfw.PRESS or action == glfw.RELEASE):
            return

        if key == glfw.KEY_SPACE:
            self.gameStart = True

        if key == glfw.KEY_ESCAPE:
            sys.exit()
        
        if (key == glfw.KEY_A or key == glfw.KEY_LEFT) and action == glfw.PRESS:
            self.snake.turn = 1
        
        elif (key == glfw.KEY_A or key == glfw.KEY_LEFT) and action == glfw.RELEASE:
            self.snake.turn = 0
        
        elif (key == glfw.KEY_D or key == glfw.KEY_LEFT) and action == glfw.PRESS:
            self.snake.turn = -1
        
        elif (key == glfw.KEY_D or key == glfw.KEY_RIGHT) and action == glfw.RELEASE:
            self.snake.turn = 0 

        elif key == glfw.KEY_R:
            self.camera.topView = False
            self.camera.headView = True
            self.camera.lolView = False

        elif key == glfw.KEY_E:
            self.camera.topView = True
            self.camera.headView = False
            self.camera.lolView = False

        elif key == glfw.KEY_T:
            self.camera.topView = False 
            self.camera.headView = False 
            self.camera.lolView = True


