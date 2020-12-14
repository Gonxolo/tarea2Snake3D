import glfw
from sys import exit
import numpy as np

import lib.transformations as tr

class Camera():
    def __init__(self):
        self.snakeView = None
        self.topView = False
        self.lolView = False
        self.headView = True
    
    def view(self):
        if self.topView:
            return tr.lookAt(
                np.array([0,0,20]),     # eye
                np.array([0.0001,0,0]), # at
                np.array([0,0,1])       # up
            )
            
        elif self.lolView:
            return tr.lookAt(
                np.array([-20,0,10]), # eye
                np.array([10,0,-20]), # at
                np.array([0,0,1])     # up
            )

        elif self.headView:
            return tr.lookAt(
                np.array([self.snakeView.x+np.cos(self.snakeView.theta)*-2, self.snakeView.y+np.sin(self.snakeView.theta)*-2,self.snakeView.z+2]),   # eye
                np.array([self.snakeView.x+np.cos(self.snakeView.theta), self.snakeView.y+np.sin(self.snakeView.theta),self.snakeView.z+1]),  # at
                np.array([0,0,1])                                        # up
            )
        
        else: return
