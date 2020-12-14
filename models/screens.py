import numpy as np
import random
from OpenGL.GL import *

import lib.basic_shapes as bs
import lib.easy_shaders as es
import lib.transformations as tr
import lib.obj_handler as obj_reader


class Screens(object):
    def __init__(self):
        self.c = 0
        self.d = 0
        self.go = True
        self.do = True
        self.GPUmenu = es.toGPUShape(obj_reader.readOBJ2("objects/snok.obj","objects/textures/text.png"), GL_REPEAT, GL_NEAREST)
        self.GPUover = es.toGPUShape(obj_reader.readOBJ2("objects/gameover.obj","objects/textures/text.png"), GL_REPEAT, GL_NEAREST)
        # self.GPUmenu = es.toGPUShape(obj_reader.readOBJ("objects/snok.obj",(0.1,0.1,0.1)), GL_REPEAT, GL_NEAREST)
        # self.GPUover = es.toGPUShape(obj_reader.readOBJ("objects/snok.obj",(0.1,0.1,0.1)), GL_REPEAT, GL_NEAREST)
        self.menuTransform = tr.matmul([tr.translate(-0.3,4.0,8.0),tr.uniformScale(2),tr.rotationX(np.pi/2),tr.rotationY(3*np.pi/2)])
        self.overTransform = tr.matmul([tr.translate(0.3,3.0,8.0),tr.uniformScale(2),tr.rotationX(np.pi/2),tr.rotationY(3*np.pi/2)])

    def mainMenu(self, pipeline, projection, view):
        glUseProgram(pipeline.shaderProgram)

        self.menuTransform = tr.matmul([tr.translate(-0.3,4.0,8.0+self.c*2),tr.rotationY(-0.25+self.c*0.5),tr.uniformScale(2),tr.rotationX(np.pi/2),tr.rotationY(3*np.pi/2)])
        if self.go:
            self.c += 0.001
            if self.c >= 1.0:
                self.go = False
        else:
            self.c -= 0.001
            if self.c <= 0.0:
                self.go = True
        # White light in all components: ambient, diffuse and specular.
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "La"), 0.45, 0.45, 0.45)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ld"), 0.45, 0.45, 0.45)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ls"), 0.45, 0.45, 0.45)

        # Setting material composition
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ka"), 0.45, 0.45, 0.45)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Kd"), 0.45, 0.45, 0.45)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ks"), 0.45, 0.45, 0.45)


        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "lightPosition"), 0, 0, 50)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "viewPosition"), 0.0, 0.0, 0)
        glUniform1ui(glGetUniformLocation(pipeline.shaderProgram, "shininess"), 100)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "constantAttenuation"), 0.001)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "linearAttenuation"), 0.0001)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "quadraticAttenuation"), 0.0001)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, self.menuTransform)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        pipeline.drawShape(self.GPUmenu)

    def gameOver(self, pipeline, projection, view):
        glUseProgram(pipeline.shaderProgram)

        self.overTransform = tr.matmul([tr.translate(0.3,3.0,8.0+self.d*2),tr.rotationY(-0.25+self.d*0.5),tr.rotationX(-0.25+self.d*0.5),tr.uniformScale(2),tr.rotationX(np.pi/2),tr.rotationY(3*np.pi/2)])
        if self.do:
            self.d += 0.001
            if self.d >= 1.0:
                self.do = False
        else:
            self.d -= 0.001
            if self.d <= 0.0:
                self.do = True
        # White light in all components: ambient, diffuse and specular.
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "La"), 0.45, 0.45, 0.45)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ld"), 0.45, 0.45, 0.45)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ls"), 0.45, 0.45, 0.45)

        # Setting material composition
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ka"), 0.45, 0.45, 0.45)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Kd"), 0.45, 0.45, 0.45)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ks"), 0.45, 0.45, 0.45)


        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "lightPosition"), 0, 0, 50)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "viewPosition"), 0.0, 0.0, 0)
        glUniform1ui(glGetUniformLocation(pipeline.shaderProgram, "shininess"), 100)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "constantAttenuation"), 0.001)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "linearAttenuation"), 0.0001)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "quadraticAttenuation"), 0.0001)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, self.overTransform)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        pipeline.drawShape(self.GPUover)