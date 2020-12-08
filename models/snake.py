import numpy as np
from OpenGL.GL import *

import lib.basic_shapes as bs
import lib.easy_shaders as es
import lib.transformations as tr
import lib.obj_handler as obj_reader


class Head():
    
    def __init__(self):
        self.x, self.y, self.z = 0.0, 0.0, -9.5
        # self.ppos = []
        self.theta = 0.0
        self.bend = 0.10
        self.front = 0.25
        self.turn = 0

        obj = "objects/dummy.obj"
        headOBJ = obj_reader.readOBJ2(f'{obj}',"objects/textures/test2.png")
        self.GPU = es.toGPUShape(headOBJ, GL_REPEAT, GL_NEAREST)
        self.transform = tr.matmul([tr.translate(0.0,0.0,-9.5),tr.uniformScale(1),tr.rotationZ(self.theta)])
    
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
        self.x += self.front*np.cos(self.theta)
        self.y += self.front*np.sin(self.theta)
        self.transform = tr.matmul([tr.translate(self.x,self.y,-9.5),tr.uniformScale(1),tr.rotationZ(self.theta)])
        
    def update(self):
        self.theta += self.bend*self.turn

class Body():
    
    def __init__(self):
        self.pos = [(0.0, 0.0)]
        self.z = -9.5     
        self.theta = [0.0]
        
        obj = "objects/dummy.obj"
        headOBJ = obj_reader.readOBJ2(f'{obj}',"img/snake.png")
        self.GPU = es.toGPUShape(headOBJ, GL_REPEAT, GL_NEAREST)
    
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
        glUniform1ui(glGetUniformLocation(pipeline.shaderProgram, "shininess"), 100000)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "constantAttenuation"), 0.001)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "linearAttenuation"), 0.0001)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "quadraticAttenuation"), 0.0001)

        for i in range(len(self.pos)):
            glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "viewPosition"), self.pos[i][0], self.pos[i][1], -9.5)

            transform = tr.matmul([tr.translate(self.pos[i][0],self.pos[i][1],-9.5),tr.uniformScale(1),tr.rotationZ(self.theta[i])])
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, transform)
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
            pipeline.drawShape(self.GPU)

    def move(self, head):
        self.pos[0] = (head.x + np.cos(self.theta[0])*-0.5, head.y + np.sin(self.theta[0])*-0.5)
        self.theta[0] = head.theta
        for i in range(1,len(self.pos)):
            self.pos[i] = (self.pos[i-1][0] + np.cos(self.theta[i])*-0.5, self.pos[i-1][1] + np.sin(self.theta[i])*-0.5)
            self.theta[i] = self.theta[i-1]
        

class Snake():
    
    def __init__(self):
        self.alive = True
        self.head = Head()
        self.body = Body()
        self.initial_size = 5
        self.length = 5
        self.objective = None
        for i in range(1,self.initial_size):
            self.body.pos.append((-0.5*i, 0.0))
            self.body.theta.append(0.0)
            # self.body.ppos = [(j,0,0) for j in np.arange(self.body.pos[i][0],self.body.pos[i-1][0]+0.1,0.1)]
            self.body.move(self.head)
            

    
    def draw(self, pipeline, projection, view):
        if not self.alive:
            return
        self.head.draw(pipeline, projection, view)
        self.body.draw(pipeline, projection, view)


    def growth(self):
        # x, y, theta = self.body.pos[-2], self.body.pos[-2], self.body.theta[-2]
        # self.body.pos[-1], self.body.pos[-1], self.body.theta[-1] = x+(np.cos(theta))*-0.5, y+(np.cos(theta))*-0.5, theta
        # xL = np.arange(self.body.pos[-1].x, x+0.1, 0.1)
        # yL = np.arange(self.body.pos[-1].y, y+0.1, 0.1)
        # self.body.pos[-1].ppos = [(xL[i],yL[i],theta) for i in range(len(xL))]
        # self.body.pos[-1].move()
        # self.length += 1
        # n = len(self.body.pos)-1
        # self.body.pos.append((-0.5*n, -0.5*n))
        print(self.length)


    def collisions(self):
        x, y = self.head.x, self.head.y

        if (x-self.objective.x)**2 + (y-self.objective.y)**2 < 1.0:
            self.objective.exists = False
            self.growth()

        # if x**2 > 100 or y**2 > 100:
        #     self.alive = False
        
        for i in range(1,len(self.body.pos)):
            if (x - self.body.pos[i][0])**2 + (y - self.body.pos[i][1])**2 < 0.1:
                self.alive = False
        

    def move(self):
        if not self.alive:
            return
        self.body.move(self.head)
        self.head.move()
        