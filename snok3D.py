# coding=utf-8

import sys

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np

import lib.transformations as tr
import lib.lighting_shaders as ls
import lib.easy_shaders as es
import lib.basic_shapes as bs

from controller import Controller
from models.list import Camera, Floor
from models.snake import *



def vista():

    # Initialize glfw
    if not glfw.init(): sys.exit()

    WIDTH = 1000; HEIGHT = 800

    window = glfw.create_window(WIDTH, HEIGHT, "Sphere", None, None)

    if not window: glfw.terminate(); sys.exit()

    glfw.make_context_current(window)

    ctrl = Controller()
    glfw.set_key_callback(window, ctrl.on_key)

    # Assembling the shader program (pipeline) with all shaders
    pipeline = es.SimpleModelViewProjectionShaderProgram()  # SIMPLE PIPELINE
    texture_pipeline = es.SimpleTextureModelViewProjectionShaderProgram() # TEXTURE PIPELINE
    lighting_pipeline = ls.SimpleTexturePhongShaderProgram() # LIGHTING PIPELINE
    
    # Telling OpenGL to use our shader program
    glUseProgram(pipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.85, 0.85, 0.85, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    # Using the same view and projection matrices in the whole application
    projection = tr.perspective(45, float(WIDTH)/float(HEIGHT), 0.1, 100)

    # MODELOS
    floor = Floor()
    snake = Snake(); ctrl.snake = snake.snake_parts[0]
    camera = Camera(); camera.snakeView = snake.snake_parts[0]; ctrl.camera = camera

    limitFPS = 1.0 / 30.0

    lastTime = 0
    timer = 0

    deltaTime = 0
    nowTime = 0
    
    frames = 0
    updates = 0

    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()
    
        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Calculamos el dt
        nowTime = glfw.get_time()
        deltaTime += (nowTime - lastTime) / limitFPS
        lastTime = nowTime

        while deltaTime >= 1.0:
            snake.snake_parts[0].update()
            snake.move()
            snake.snake_parts[0].move()
            updates += 1     
            deltaTime -= 1.0


        view = camera.view()

        glUseProgram(lighting_pipeline.shaderProgram)
        floor.draw(lighting_pipeline, projection, view) 
        snake.draw(lighting_pipeline, projection, view)
        
        # sGPU = es.toGPUShape(bs.createTextureCube('img/background_tile.png'), GL_REPEAT, GL_NEAREST)
        # stransform = tr.matmul([tr.translate(0.0,0.0,-8.5),tr.scale(1,1,2),tr.uniformScale(1)])
        # glUniformMatrix4fv(glGetUniformLocation(texture_pipeline.shaderProgram, "model"), 1, GL_TRUE, stransform)
        # glUniformMatrix4fv(glGetUniformLocation(texture_pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        # glUniformMatrix4fv(glGetUniformLocation(texture_pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        # texture_pipeline.drawShape(sGPU)
    
        frames += 1

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

        if glfw.get_time() - timer > 1.0:
            timer += 1
            print("FPS: ",frames," Updates: ",updates)
            updates = 0
            frames = 0

    
    glfw.terminate()


if __name__ == "__main__":
    vista()