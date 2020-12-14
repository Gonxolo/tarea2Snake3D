import numpy as np
import random
from OpenGL.GL import *

import lib.basic_shapes as bs
import lib.easy_shaders as es
import lib.transformations as tr
import lib.obj_handler as obj_reader


class Vinyl():
    def __init__(self):
        self.x, self.y, self.z = 0.0, 0.0, -4.5
        self.exists = False
        self.theta = 0.0
        self.rare = 0
        self.bans = [(None,None,None)]
        self.GPU = es.toGPUShape(obj_reader.readOBJ('objects/record.obj', (1.0,1.0,1.0)), GL_REPEAT, GL_NEAREST)
        self.transform = tr.matmul([tr.translate(0.0,0.0,self.z),tr.uniformScale(1),tr.rotationZ(self.theta),tr.rotationX(np.pi/4)])

    def spawn(self):
        self.x = random.uniform(-8,8)
        self.y = random.uniform(-8,8)
        while not self.posChecker():
            self.x = random.uniform(-8,8)
            self.y = random.uniform(-8,8)
            self.posChecker()
        self.exists = True
        
    def posChecker(self):
        for pos in self.bans:
            if (pos[0]-self.x)**2 < 1.0:
                if (pos[1]-self.y)**2 < 1.0:
                    return False
        return True        

    def draw(self, pipeline, projection, view):
        glUseProgram(pipeline.shaderProgram)

        if self.rare%5 == 4:
            # White light in all components: ambient, diffuse and specular.
            glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "La"), 1.0, 215/255, 0.0)
            glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ld"), 0.0, 0.0, 0.0)
            glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ls"), 1.0, 1.0, 1.0)

            # Object is barely visible at only ambient. Bright white for diffuse and specular components.
            glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ka"), 1.0, 1.0, 1.0)
            glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Kd"), 0.6, 0.6, 0.6)
            glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ks"), 0.6, 0.6, 0.6)
        else:
            # White light in all components: ambient, diffuse and specular.
            glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "La"), 0.0, 0.0, 0.0)
            glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ld"), 0.01, 0.01, 0.01)
            glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ls"), 0.0, 0.0, 0.0)

            # Object is barely visible at only ambient. Bright white for diffuse and specular components.
            glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ka"), 0.0, 0.0, 0.0)
            glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Kd"), 1.0, 1.0, 1.0)
            glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ks"), 0.0, 0.0, 0.0)

        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "lightPosition"), 0, 0, 50)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "viewPosition"), self.x, self.y, self.z)
        glUniform1ui(glGetUniformLocation(pipeline.shaderProgram, "shininess"), 100000)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "constantAttenuation"), 0.001)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "linearAttenuation"), 0.0001)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "quadraticAttenuation"), 0.0001)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, self.transform)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        pipeline.drawShape(self.GPU)

    def update(self):
        self.theta += 0.1
        self.transform = tr.matmul([tr.translate(self.x,self.y,self.z),tr.uniformScale(0.5),tr.rotationZ(self.theta),tr.rotationX(np.pi/4)])
