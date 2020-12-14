import os

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
        self.GPUmenu = es.toGPUShape(obj_reader.readOBJ2(os.path.join("objects","snok.obj"),os.path.join("objects","textures","text.png")), GL_REPEAT, GL_NEAREST)
        self.GPUuntitled = es.toGPUShape(obj_reader.readOBJ(os.path.join("objects","untitled.obj"), (1.0, 1.0, 1.0)), GL_REPEAT, GL_NEAREST)
        self.GPUover = es.toGPUShape(obj_reader.readOBJ2(os.path.join("objects","gameover.obj"),os.path.join("objects","textures","text.png")), GL_REPEAT, GL_NEAREST)
        self.menuTransform = tr.matmul([tr.translate(0.0,0.0,8.0),tr.uniformScale(2),tr.rotationX(np.pi/2),tr.rotationY(3*np.pi/2)])
        self.untitledTransform = tr.matmul([tr.translate(-2.0,0.0,8.0),tr.uniformScale(1.5),tr.rotationX(np.pi/2),tr.rotationY(3*np.pi/2)])
        self.overTransform = tr.matmul([tr.translate(0.0,0.0,8.0),tr.uniformScale(2),tr.rotationX(np.pi/2),tr.rotationY(3*np.pi/2)])

    def mainMenu(self, pipeline, projection, view, phong_pipeline):
        glUseProgram(pipeline.shaderProgram)

        self.menuTransform = tr.matmul([tr.translate(2.0,0.0,8.0+self.c*2),tr.rotationY(-0.25+self.c*0.5),tr.uniformScale(2),tr.rotationX(np.pi/2),tr.rotationY(3*np.pi/2)])
        if self.go:
            self.c += 0.001
            if self.c >= 1.0:
                self.go = False
        else:
            self.c -= 0.001
            if self.c <= 0.0:
                self.go = True

        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "La"), 0.85, 0.85, 0.85)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ld"), 0.0, 0.0, 0.0)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ls"), 0.2, 0.2, 0.2)

        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ka"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Kd"), 0.0, 0.0, 0.0)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ks"), 1.0, 0.0, 1.0)


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

        glUseProgram(phong_pipeline.shaderProgram)
        
        glUniform3f(glGetUniformLocation(phong_pipeline.shaderProgram, "La"), 0.0, 0.0, 0.0)
        glUniform3f(glGetUniformLocation(phong_pipeline.shaderProgram, "Ld"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(phong_pipeline.shaderProgram, "Ls"), 0.0, 0.0, 0.0)

        glUniform3f(glGetUniformLocation(phong_pipeline.shaderProgram, "Ka"), 0.0, 0.0, 0.0)
        glUniform3f(glGetUniformLocation(phong_pipeline.shaderProgram, "Kd"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(phong_pipeline.shaderProgram, "Ks"), 0.0, 0.0, 0.0)


        glUniform3f(glGetUniformLocation(phong_pipeline.shaderProgram, "lightPosition"), 0, 0, 50)
        glUniform3f(glGetUniformLocation(phong_pipeline.shaderProgram, "viewPosition"), 0.0, 0.0, 0)
        glUniform1ui(glGetUniformLocation(phong_pipeline.shaderProgram, "shininess"), 100)
        glUniform1f(glGetUniformLocation(phong_pipeline.shaderProgram, "constantAttenuation"), 0.001)
        glUniform1f(glGetUniformLocation(phong_pipeline.shaderProgram, "linearAttenuation"), 0.0001)
        glUniform1f(glGetUniformLocation(phong_pipeline.shaderProgram, "quadraticAttenuation"), 0.0001)

        glUniformMatrix4fv(glGetUniformLocation(phong_pipeline.shaderProgram, "model"), 1, GL_TRUE, self.untitledTransform)
        glUniformMatrix4fv(glGetUniformLocation(phong_pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(phong_pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        phong_pipeline.drawShape(self.GPUuntitled)

    def gameOver(self, pipeline, projection, view):
        glUseProgram(pipeline.shaderProgram)

        self.overTransform = tr.matmul([tr.translate(0.0,0.0,8.0+self.d*2),tr.rotationY(-0.25+self.d*0.5),tr.rotationX(-0.25+self.d*0.5),tr.uniformScale(2),tr.rotationX(np.pi/2),tr.rotationY(3*np.pi/2)])
        if self.do:
            self.d += 0.001
            if self.d >= 1.0:
                self.do = False
        else:
            self.d -= 0.001
            if self.d <= 0.0:
                self.do = True

        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "La"), 0.85, 0.85, 0.85)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ld"), 0.0, 0.0, 0.0)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ls"), 0.2, 0.2, 0.2)

        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ka"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Kd"), 0.0, 0.0, 0.0)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ks"), 1.0, 0.0, 1.0)


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