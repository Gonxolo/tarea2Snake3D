import numpy as np
import random
from OpenGL.GL import *

import lib.basic_shapes as bs
import lib.easy_shaders as es
import lib.transformations as tr
import lib.obj_handler as obj_reader


class Screens(object):
    def __init__(self):
        # self.GPUmenu = es.toGPUShape(obj_reader.readOBJ2("objects/snok!.obj","objects/textures/text.png"), GL_REPEAT, GL_NEAREST)
        # self.GPUover = es.toGPUShape(obj_reader.readOBJ2("objects/snok!.obj","objects/textures/text.png"), GL_REPEAT, GL_NEAREST)
        self.GPUmenu = es.toGPUShape(obj_reader.readOBJ("objects/snok.obj",(0.1,0.1,0.1)), GL_REPEAT, GL_NEAREST)
        self.GPUover = es.toGPUShape(obj_reader.readOBJ("objects/snok.obj",(0.1,0.1,0.1)), GL_REPEAT, GL_NEAREST)
        self.menuTransform = tr.matmul([tr.translate(0.0,0.0,-9.5),tr.uniformScale(1)])#,tr.rotationZ(self.theta)])
        self.overTransform = tr.matmul([tr.translate(0.0,0.0,-9.5),tr.uniformScale(1)])#,tr.rotationZ(self.theta)])

    def mainMenu(self, pipeline, projection, view):
        glUseProgram(pipeline.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, self.menuTransform)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        pipeline.drawShape(self.GPUmenu)

    def gameOver(self, pipeline, projection, view):
        glUseProgram(pipeline.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, self.overTransform)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        pipeline.drawShape(self.GPUover)