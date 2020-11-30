import numpy as np
from OpenGL.GL import *

import lib.basic_shapes as bs
import lib.easy_shaders as es
import lib.transformations as tr


class Snake():
    
    def __init__(self):
        self.x, self.y = 0, 0
        self.theta = 0
        self.bend = 0.10
        self.front = 0.075
        self.turn = 0
        self.GPU = es.toGPUShape(bs.createTextureCube('img/snake.png'), GL_REPEAT, GL_NEAREST)
        self.transform = tr.matmul([tr.translate(0.0,0.0,-8.0),tr.uniformScale(2),tr.rotationZ(self.theta)])
    
    def draw(self, texture_pipeline, projection, view):
        glUseProgram(texture_pipeline.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(texture_pipeline.shaderProgram, "model"), 1, GL_TRUE, self.transform)
        glUniformMatrix4fv(glGetUniformLocation(texture_pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(texture_pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        texture_pipeline.drawShape(self.GPU)
    def move(self):
        self.x += self.front*np.cos(self.theta)
        self.y += self.front*np.sin(self.theta)
        self.transform = tr.matmul([tr.translate(self.x,self.y,-8.0),tr.uniformScale(2),tr.rotationZ(self.theta)])
    def update(self):
        self.theta += self.bend*self.turn