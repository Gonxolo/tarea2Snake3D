# coding=utf-8

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys

from controller import ctrl
from controller import on_key as _on_key
import model

import transformations as tr
import lighting_shaders as ls
import easy_shaders as es
import basic_shapes as bs


if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 800
    height = 800

    window = glfw.create_window(width, height, "Sphere", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, _on_key)

    # Assembling the shader program (pipeline) with both shaders
    pipeline = es.SimpleModelViewProjectionShaderProgram()
    texture_pipeline = es.SimpleTextureModelViewProjectionShaderProgram()
    
    # Telling OpenGL to use our shader program
    glUseProgram(pipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.85, 0.85, 0.85, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    # Using the same view and projection matrices in the whole application
    projection = tr.perspective(45, float(width)/float(height), 0.1, 100)

    # Generaremos diversas cámaras.
    static_view = tr.lookAt(
            #np.array([10,10,5]), # eye
            np.array([0,0,10]), # eye
            np.array([0,0.0001,0]), # at
            np.array([0,0,1])  # up
        )

    skyBox = bs.createTextureCube('skybox.png')
    sun = model.generateSun(20, 20)
    floor = bs.createTextureCube('img/rainbow1.png')

    GPUsun = es.toGPUShape(sun)
    GPUSkyBox = es.toGPUShape(skyBox, GL_REPEAT, GL_LINEAR)
    GPUfloor = es.toGPUShape(floor, GL_REPEAT, GL_NEAREST)

    skybox_transform = tr.uniformScale(20)
    floor_transform = tr.matmul([tr.translate(0,0,-10),tr.scale(16.2,16.2,1),tr.uniformScale(1)])

    t0 = glfw.get_time()
    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()
        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1
        ctrl.updatePos(t0)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if ctrl.followSun:
            view =  tr.lookAt(
                np.array([10,10,5]),
                np.array([0,0,0]),#ctrl.sunPos,  # The camera will be the sun
                np.array([0,0,1])
        )

        else:
            view = static_view


        glUseProgram(texture_pipeline.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(texture_pipeline.shaderProgram, "model"), 1, GL_TRUE, skybox_transform)
        glUniformMatrix4fv(glGetUniformLocation(texture_pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(texture_pipeline.shaderProgram, "view"), 1, GL_TRUE, view)

        texture_pipeline.drawShape(GPUSkyBox)
        

        glUseProgram(texture_pipeline.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(texture_pipeline.shaderProgram, "model"), 1, GL_TRUE, floor_transform)
        glUniformMatrix4fv(glGetUniformLocation(texture_pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(texture_pipeline.shaderProgram, "view"), 1, GL_TRUE, view)

        texture_pipeline.drawShape(GPUfloor)
        

        # Telling OpenGL to use our shader program
        glUseProgram(pipeline.shaderProgram)
        transform = tr.translate(*ctrl.sunPos)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, transform)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)


        #pipeline.drawShape(GPUsun)
        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    
    glfw.terminate()
