import numpy as np
from OpenGL.GL import *

import lib.basic_shapes as bs
import lib.easy_shaders as es
import lib.transformations as tr
import lib.obj_handler as obj_reader


class Head():
    
    def __init__(self):
        self.x, self.y, self.z = 0.0, 0.0, -9.5
        self.theta0 = 0.0 #THETA
        self.theta1 = 0.0
        self.bend = 0.3
        self.front = 0.25 #RHO
        self.turn = 0 
        self.objective = None

        obj = "objects/dummy.obj"
        headOBJ = obj_reader.readOBJ2(f'{obj}',"objects/textures/test2.png")
        self.GPU = es.toGPUShape(headOBJ, GL_REPEAT, GL_NEAREST)
        self.transform = tr.matmul([tr.translate(0.0,0.0,-9.5),tr.uniformScale(1),tr.rotationZ(self.theta0)])
    
    def draw(self, pipeline, projection, view):
        glUseProgram(pipeline.shaderProgram)

        # # White light in all components: ambient, diffuse and specular.
        # glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "La"), 0.55, 0.55, 0.55)
        # glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ld"), 0.65, 0.65, 0.65)
        # glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ls"), 0.4, 0.4, 0.4)

        # # Setting material composition
        # glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ka"), 0.25, 0.25, 0.25)
        # glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Kd"), 0.6, 0.6, 0.6)
        # glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ks"), 0.6, 0.6, 0.6)
        # White light in all components: ambient, diffuse and specular.
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "La"), 1.0,1.0,1.0)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ld"), 1.0,1.0,1.0)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ls"), 1.0,1.0,1.0)

        # Setting material composition
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ka"), 1.0,1.0,1.0)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Kd"), 1.0,1.0,1.0)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ks"), 1.0,1.0,1.0)

        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "lightPosition"), 0, 0, 50)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "viewPosition"), self.x, self.y, 0)
        glUniform1ui(glGetUniformLocation(pipeline.shaderProgram, "shininess"), 100)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "constantAttenuation"), 0.001)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "linearAttenuation"), 0.0001)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "quadraticAttenuation"), 0.0001)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, self.transform)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        pipeline.drawShape(self.GPU)

    def move(self):
        self.x += self.front*np.cos(self.theta0)
        self.y += self.front*np.sin(self.theta0)
        self.transform = tr.matmul([tr.translate(self.x,self.y,-9.5),tr.uniformScale(1),tr.rotationZ(self.theta0)])
        
    def update(self):
        self.theta1 = self.theta0
        self.theta0 += self.bend*self.turn
        print(self.theta0, self.theta1)

class Body():
    
    def __init__(self):
        self.x, self.y, self.z = 0.0, 0.0, -9.5
        self.ppos = [(None,None,None)]        
        self.theta0 = 0.0
        self.theta1 = 0.0
        
        obj = "objects/dummy.obj"
        headOBJ = obj_reader.readOBJ2(f'{obj}',"img/snake.png")
        self.GPU = es.toGPUShape(headOBJ, GL_REPEAT, GL_NEAREST)
        self.transform = tr.matmul([tr.translate(0.0,0.0,-9.5),tr.uniformScale(1),tr.rotationZ(self.theta0)])
    
    def draw(self, pipeline, projection, view):
        glUseProgram(pipeline.shaderProgram)

        # White light in all components: ambient, diffuse and specular.
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "La"), 0.55, 0.55, 0.55)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ld"), 0.65, 0.65, 0.65)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ls"), 0.4, 0.4, 0.4)

        # Object is barely visible at only ambient. Bright white for diffuse and specular components.
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ka"), 0.25, 0.25, 0.25)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Kd"), 0.6, 0.6, 0.6)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ks"), 0.6, 0.6, 0.6)

        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "lightPosition"), 50,50 ,50)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "viewPosition"), self.x, self.y, -9.5)
        glUniform1ui(glGetUniformLocation(pipeline.shaderProgram, "shininess"), 100000)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "constantAttenuation"), 0.001)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "linearAttenuation"), 0.0001)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "quadraticAttenuation"), 0.0001)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, self.transform)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        pipeline.drawShape(self.GPU)

    def move(self):
        self.transform = tr.matmul([tr.translate(self.x,self.y,-9.5),tr.rotationZ(self.theta0)])
        

class Snake():
    
    def __init__(self):
        self.alive = True
        self.snake_parts = [Head()]
        self.initial_size = 10
        for i in range(self.initial_size-1):
            self.snake_parts.append(Body())
        for i in range(1,self.initial_size):
            self.snake_parts[i].x += -0.5*i
            self.snake_parts[i].move()
            

    
    def draw(self, pipeline, projection, view):
        if not self.alive:
            return
        for part in self.snake_parts:
            part.draw(pipeline, projection, view)


    def growth(self):
        print("+1")
        # new_part = Body()
        # new_part.x = self.snake_parts[-1].x
        # new_part.y = self.snake_parts[-1].y
        # new_part.parts = self.snake_parts[-1].theta
        # new_part.move()
        # self.snake_parts.append(new_part)


    def collisions(self):
        x, y = self.snake_parts[0].x, self.snake_parts[0].y

        if (x-self.objective.x)**2 + (y-self.objective.y)**2 < 1.0:
            self.objective.exists = False
            self.growth()

        # if x**2 > 100 or y**2 > 100:
        #     self.alive = False
        
        for i in range(1,len(self.snake_parts)):
            if (x - self.snake_parts[i].x)**2 + (y - self.snake_parts[i].y)**2 < 0.2:
                self.alive = False
        

    def move(self):
        if not self.alive:
            return

        for i in range(1,len(self.snake_parts)):
            self.snake_parts[i].theta1 = self.snake_parts[i].theta0
            self.snake_parts[i].theta0 = self.snake_parts[i-1].theta1
            self.snake_parts[i].x = self.snake_parts[i-1].x + 0.5*np.cos(self.snake_parts[i].theta0+np.pi)
            self.snake_parts[i].y = self.snake_parts[i-1].y + 0.5*np.sin(self.snake_parts[i].theta0+np.pi)
            self.snake_parts[i].move()
        
        # self.collisions()

        