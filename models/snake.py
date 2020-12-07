import numpy as np
from OpenGL.GL import *

import lib.basic_shapes as bs
import lib.easy_shaders as es
import lib.transformations as tr
import lib.obj_handler as obj_reader


# def slerp(v0, v1, t_array):
#     """Spherical linear interpolation."""
#     # >>> slerp([1,0,0,0], [0,0,0,1], np.arange(0, 1, 0.001))
#     t_array = np.array(t_array)
#     v0 = np.array(v0)
#     v1 = np.array(v1)
#     dot = np.sum(v0 * v1)

#     if dot < 0.0:
#         v1 = -v1
#         dot = -dot
    
#     DOT_THRESHOLD = 0.9995
#     if dot > DOT_THRESHOLD:
#         result = v0[np.newaxis,:] + t_array[:,np.newaxis] * (v1 - v0)[np.newaxis,:]
#         return (result.T / np.linalg.norm(result, axis=1)).T
    
#     theta_0 = np.arccos(dot)
#     sin_theta_0 = np.sin(theta_0)

#     theta = theta_0 * t_array
#     sin_theta = np.sin(theta)
    
#     s0 = np.cos(theta) - dot * sin_theta / sin_theta_0
#     s1 = sin_theta / sin_theta_0
#     return (s0[:,np.newaxis] * v0[np.newaxis,:]) + (s1[:,np.newaxis] * v1[np.newaxis,:])

class Head():
    
    def __init__(self):
        self.x, self.y, self.z = 0.0, 0.0, -7.0
        self.ppos = []
        self.theta = 0.0
        self.bend = 0.10
        self.front = 0.25
        self.turn = 0

        obj = "objects/dummy.obj"
        headOBJ = obj_reader.readOBJ2(f'{obj}',"img/background_tile.png")
        self.GPU = es.toGPUShape(headOBJ, GL_REPEAT, GL_NEAREST)
        self.transform = tr.matmul([tr.translate(0.0,0.0,-7.0),tr.uniformScale(1),tr.rotationZ(self.theta)])
    
    def draw(self, pipeline, projection, view):
        glUseProgram(pipeline.shaderProgram)

        # White light in all components: ambient, diffuse and specular.
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "La"), 0.55, 0.55, 0.55)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ld"), 0.65, 0.65, 0.65)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ls"), 0.4, 0.4, 0.4)

        # Setting material composition
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ka"), 0.25, 0.25, 0.25)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Kd"), 0.6, 0.6, 0.6)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ks"), 0.6, 0.6, 0.6)

        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "lightPosition"), 50,50 ,50)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "viewPosition"), self.x, self.y, 0)
        glUniform1ui(glGetUniformLocation(pipeline.shaderProgram, "shininess"), 100000)
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
        self.transform = tr.matmul([tr.translate(self.x,self.y,-7.0),tr.uniformScale(1),tr.rotationZ(self.theta)])
        
    def update(self):
        self.theta += self.bend*self.turn

class Body():
    
    def __init__(self):
        self.x, self.y, self.z = 0.0, 0.0, -7.0
        self.ppos = [(None,None,None)]        
        self.theta = 0.0
        
        obj = "objects/dummy.obj"
        headOBJ = obj_reader.readOBJ2(f'{obj}',"img/snake.png")
        self.GPU = es.toGPUShape(headOBJ, GL_REPEAT, GL_NEAREST)
        self.transform = tr.matmul([tr.translate(0.0,0.0,-7.0),tr.uniformScale(1),tr.rotationZ(self.theta)])
    
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
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "viewPosition"), self.x, self.y, -7.0)
        glUniform1ui(glGetUniformLocation(pipeline.shaderProgram, "shininess"), 100000)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "constantAttenuation"), 0.001)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "linearAttenuation"), 0.0001)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "quadraticAttenuation"), 0.0001)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, self.transform)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        pipeline.drawShape(self.GPU)

    def move(self):
        self.transform = tr.matmul([tr.translate(self.x,self.y,-7.0),tr.rotationZ(self.theta)])
        

class Snake():
    
    def __init__(self):
        self.alive = True
        self.snake_parts = [Head()]
        self.initial_size = 5
        for i in range(self.initial_size-1):
            self.snake_parts.append(Body())
        for i in range(1,self.initial_size):
            self.snake_parts[i].x += -0.5*i
            self.snake_parts[i].ppos = [(j,0,0) for j in np.arange(self.snake_parts[i].x,self.snake_parts[i-1].x,0.1)]
            self.snake_parts[i].move()
            

    
    def draw(self, pipeline, projection, view):
        if not self.alive:
            return
        for part in self.snake_parts:
            part.draw(pipeline, projection, view)


    def growth(self):
        new_part = Body()
        new_part.x = self.snake_parts[-1].x
        new_part.y = self.snake_parts[-1].y
        new_part.parts = self.snake_parts[-1].theta
        new_part.move()
        self.snake_parts.append(new_part)


    def collisions(self):
        x, y = self.snake_parts[0].x, self.snake_parts[0].y
        if x**2 > 100 or y**2 > 100:
            self.alive = False
        
        for i in range(1,self.snake_parts):
            if (x - self.snake_parts[i].x)**2 + (y - self.snake_parts[i].y)**2 < 0.5:
                self.alive = False
        

    def move(self):
        if not self.alive:
            return

        for i in range(1,len(self.snake_parts)):
            self.snake_parts[i].x, self.snake_parts[i].y, self.snake_parts[i].theta = self.snake_parts[i].ppos[0]
            self.snake_parts[i].ppos.pop(0)
            self.snake_parts[i].ppos.append((self.snake_parts[i-1].x, self.snake_parts[i-1].y, self.snake_parts[i-1].theta))
            self.snake_parts[i].move()
        # for i in range(len(self.snake_parts)-1,0,-1):
        #     x = self.snake_parts[i-1].x
        #     y = self.snake_parts[i-1].y
        #     theta = self.snake_parts[i-1].theta
        #     self.snake_parts[i].x = x
        #     self.snake_parts[i].y = y
        #     self.snake_parts[i].theta = theta
        #     self.snake_parts[i].move()
        #self.snake_parts[0].move()

        ### Useless slerp, maybe later if enough time
        # for i in range(1,len(self.snake_parts)):
        #     curBodyPart = self.snake_parts[i]
        #     prevBodyPart = self.snake_parts[i-1]

        #     v0 = [curBodyPart.x, curBodyPart.y, curBodyPart.z, curBodyPart.theta]
        #     v1 = [prevBodyPart.x, prevBodyPart.y, prevBodyPart.z, prevBodyPart.theta]
        #     t_array = [0.25, 0.5, 0.75, 1.0]

        #     (curBodyPart.x, curBodyPart.y, curBodyPart.z, curBodyPart.theta) = slerp(v0, v1, t_array)[0]
        #     # a = slerp(v0, v1, t_array)[0]
        #     # print(a)
        #     curBodyPart.move()
        