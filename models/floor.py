import os

import numpy as np
from OpenGL.GL import *

import lib.basic_shapes as bs
import lib.easy_shaders as es
import lib.transformations as tr


# FLOOR
class Floor():

    def __init__(self):
        self.GPUfloor1 = es.toGPUShape(bs.createTextureNormalsCube(os.path.join("img","rainbow1.png")), GL_REPEAT, GL_NEAREST)
        self.GPUfloor2 = es.toGPUShape(bs.createTextureNormalsCube(os.path.join("img","rainbow2.png")), GL_REPEAT, GL_NEAREST)
        self.GPUfloor3 = es.toGPUShape(bs.createTextureNormalsCube(os.path.join("img","rainbow3.png")), GL_REPEAT, GL_NEAREST)
        self.GPUfloor4 = es.toGPUShape(bs.createTextureNormalsCube(os.path.join("img","rainbow4.png")), GL_REPEAT, GL_NEAREST)
        self.GPUfloor5 = es.toGPUShape(bs.createTextureNormalsCube(os.path.join("img","rainbow5.png")), GL_REPEAT, GL_NEAREST)
        self.transform = tr.matmul([tr.translate(0,0,-5),tr.scale(20,20,0.001),tr.uniformScale(1)])
        self.r, self.g, self.b = np.random.random_sample(), np.random.random_sample(), np.random.random_sample()
        self.weirdTimer = 0
        self.timer = 0
        self.floorPicker = 0
    
    def draw(self, pipeline, projection, view):             

        if self.weirdTimer == 0:
            glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "La"), 1.0, 1.0, 1.0)
            glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ld"), 0.0, 0.0, 0.0)
            glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ls"), 0.0, 0.0, 0.0)

            glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ka"), 0.75, 0.75, 0.75)
            glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Kd"), 0.0, 0.0, 0.0)
            glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ks"), 0.0, 0.0, 0.0)
        
        elif self.weirdTimer > 0:
            glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "La"), self.r, self.g, self.b)
            glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ld"), 0.0, 0.0, 0.0)
            glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ls"), 0.0, 0.0, 0.0)

            glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ka"), 0.75, 0.75, 0.75)
            glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Kd"), 0.0, 0.0, 0.0)
            glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ks"), 0.0, 0.0, 0.0)

        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "lightPosition"), 0,0 ,20)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "viewPosition"), 0, 0, 0)
        glUniform1ui(glGetUniformLocation(pipeline.shaderProgram, "shininess"), 1)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "constantAttenuation"), 0.01)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "linearAttenuation"), 0.01)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "quadraticAttenuation"), 0.01)

        glUseProgram(pipeline.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, self.transform)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)

        if self.floorPicker%5 == 0:
            pipeline.drawShape(self.GPUfloor1)
        elif self.floorPicker%5 == 1:
            pipeline.drawShape(self.GPUfloor2)
        elif self.floorPicker%5 == 2:
            pipeline.drawShape(self.GPUfloor3)
        elif self.floorPicker%5 == 3:
            pipeline.drawShape(self.GPUfloor4)
        elif self.floorPicker%5 == 4:
            pipeline.drawShape(self.GPUfloor5)

    def update(self):
        self.r, self.g, self.b = np.random.random_sample(), np.random.random_sample(), np.random.random_sample()