import os

import numpy as np
from OpenGL.GL import *

import lib.basic_shapes as bs
import lib.easy_shaders as es
import lib.transformations as tr
import lib.obj_handler as obj_reader

from collections import deque


class Head():
    
    def __init__(self):
        self.x, self.y, self.z = 0.0, 0.0, -4.5
        self.theta = 0.0
        self.bend = 0.20
        self.front = 0.20
        self.turn = 0
        self.weirdLight = (1.0, 1.0, 1.0)
        self.transform = tr.matmul([tr.translate(self.x,self.y,self.z),tr.uniformScale(0.5),tr.rotationZ(self.theta)])
    
    def draw(self, objeto, pipeline, projection, view):
        glUseProgram(pipeline.shaderProgram)

        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "La"), 0.25*self.weirdLight[0], 0.25*self.weirdLight[1], 0.25*self.weirdLight[2])
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ld"), 0.65*self.weirdLight[0], 0.65*self.weirdLight[1], 0.65*self.weirdLight[2])
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ls"), 0.1*self.weirdLight[0], 0.1*self.weirdLight[1], 0.1*self.weirdLight[2])

        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ka"), 0.25, 0.25, 0.25)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Kd"), 0.6, 0.6, 0.6)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ks"), 1.0, 1.0, 1.0)


        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "lightPosition"), 0, 0, 50)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "viewPosition"), self.x,self.y,self.z)
        glUniform1ui(glGetUniformLocation(pipeline.shaderProgram, "shininess"), 100)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "constantAttenuation"), 0.001)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "linearAttenuation"), 0.0001)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "quadraticAttenuation"), 0.0001)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, self.transform)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        pipeline.drawShape(objeto)

    def move(self):
        self.x += self.front*np.cos(self.theta)
        self.y += self.front*np.sin(self.theta)
        self.transform = tr.matmul([tr.translate(self.x,self.y,self.z),tr.uniformScale(0.5),tr.rotationZ(self.theta)])

        
    def update(self):
        self.theta += self.bend*self.turn

class Body():
    
    def __init__(self):
        self.x, self.y, self.z = 0.0, 0.0, -4.5
        self.theta = 0.0
        self.transform = tr.matmul([tr.translate(self.x,self.y,self.z),tr.uniformScale(0.5),tr.rotationZ(self.theta)])
        self.weirdLight = (1.0, 1.0, 1.0)
    
    def draw(self, objeto, pipeline, projection, view):
        glUseProgram(pipeline.shaderProgram)

        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "La"), 0.25*self.weirdLight[0], 0.25*self.weirdLight[1], 0.25*self.weirdLight[2])
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ld"), 0.65*self.weirdLight[0], 0.65*self.weirdLight[1], 0.65*self.weirdLight[2])
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ls"), 0.1*self.weirdLight[0], 0.1*self.weirdLight[1], 0.1*self.weirdLight[2])

        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ka"), 0.25, 0.25, 0.25)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Kd"), 0.6, 0.6, 0.6)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ks"), 1.0, 1.0, 1.0)

        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "lightPosition"), 0, 0, 50)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "viewPosition"), self.x, self.y, self.z)
        glUniform1ui(glGetUniformLocation(pipeline.shaderProgram, "shininess"), 100)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "constantAttenuation"), 0.001)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "linearAttenuation"), 0.0001)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "quadraticAttenuation"), 0.0001)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, self.transform)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        pipeline.drawShape(objeto)

    def move(self):
        self.transform = tr.matmul([tr.translate(self.x,self.y,self.z),tr.uniformScale(0.5),tr.rotationZ(self.theta)])
              

class Snake():
    
    def __init__(self):
        self.alive = True
        self.objective = None
        self.floor = None
        self.snake_parts = [Head()]
        self.bodyTypeList = [1,0,2,3,4]
        self.weirdLight = (1.0, 1.0, 1.0)
        obj = os.path.join("objects","dummy.obj")
        bodyOBJ1 = obj_reader.readOBJ2(f'{obj}',os.path.join("objects","textures","dudeBlack.png"))
        bodyOBJ2 = obj_reader.readOBJ2(f'{obj}',os.path.join("objects","textures","dudeRed.png"))
        bodyOBJ3 = obj_reader.readOBJ2(f'{obj}',os.path.join("objects","textures","dudeWhite.png"))
        bodyOBJ4 = obj_reader.readOBJ2(f'{obj}',os.path.join("objects","textures","dudeOrange.png"))
        bodyOBJ5 = obj_reader.readOBJ2(f'{obj}',os.path.join("objects","textures","dudeGreen.png"))
        self.GPU1 = es.toGPUShape(bodyOBJ1, GL_REPEAT, GL_NEAREST)
        self.GPU2 = es.toGPUShape(bodyOBJ2, GL_REPEAT, GL_NEAREST)
        self.GPU3 = es.toGPUShape(bodyOBJ3, GL_REPEAT, GL_NEAREST)
        self.GPU4 = es.toGPUShape(bodyOBJ4, GL_REPEAT, GL_NEAREST)
        self.GPU5 = es.toGPUShape(bodyOBJ5, GL_REPEAT, GL_NEAREST)
        self.positions = deque([])
        self.initial_size = 5
        self.length = 5
        for i in range(self.initial_size-1):
            self.snake_parts.append(Body())

        for i in range(1,self.initial_size):
            self.snake_parts[i].x += -0.3*i
            for j in np.arange(self.snake_parts[i-1].x,self.snake_parts[i].x,-0.1):
                self.positions.appendleft((j,0,0))
            self.snake_parts[i].move()
            
    def lightChange(self):
        for part in self.snake_parts:
            part.weirdLight = self.weirdLight
    
    def draw(self, pipeline, projection, view):
        if not self.alive:
            return
        for i in range(len(self.snake_parts)):
            if self.bodyTypeList[i] % 5 == 0:
                self.snake_parts[i].draw(self.GPU1, pipeline, projection, view)
            if self.bodyTypeList[i] % 5 == 1:
                self.snake_parts[i].draw(self.GPU2, pipeline, projection, view)
            if self.bodyTypeList[i] % 5 == 2:
                self.snake_parts[i].draw(self.GPU3, pipeline, projection, view)
            if self.bodyTypeList[i] % 5 == 3:
                self.snake_parts[i].draw(self.GPU4, pipeline, projection, view)
            if self.bodyTypeList[i] % 5 == 4:
                self.snake_parts[i].draw(self.GPU5, pipeline, projection, view)


    def growth(self):
        new_part = Body()
        self.snake_parts.append(new_part)
        self.snake_parts[-1].x, self.snake_parts[-1].y, self.snake_parts[-1].theta = self.positions[(self.length-1)*-3]
        self.snake_parts[-1].move()
        roll = np.random.randint(0,4)
        self.bodyTypeList.append(roll)
        self.length += 1


    def collisions(self):
        x, y = self.snake_parts[0].x, self.snake_parts[0].y

        if (x-self.objective.x)**2 + (y-self.objective.y)**2 < 1.0:
            if self.objective.rare%5 == 0:
                self.floor.weirdTimer += 200
            self.objective.exists = False
            self.objective.rare += 1
            self.growth()

        if x**2 > 100 or y**2 > 100:
            self.alive = False

        for i in range(1,len(self.snake_parts)):
            if (x - self.snake_parts[i].x)**2 + (y - self.snake_parts[i].y)**2 < 0.09:
                self.alive = False


    def move(self):
        if not self.alive:
            return
        for i in range(1,self.length):
            self.snake_parts[i].x, self.snake_parts[i].y, self.snake_parts[i].theta = self.positions[i*-3]
            self.snake_parts[i].move()
        self.snake_parts[0].update()
        self.snake_parts[0].move()
        self.positions.append((self.snake_parts[0].x,self.snake_parts[0].y,self.snake_parts[0].theta))
        while len(self.positions) > self.length * 10:
            self.positions.popleft()
        
        