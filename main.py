from scene import Scene
import taichi as ti
from taichi.math import *

scene = Scene(voxel_edges=0, exposure=2)
scene.set_floor(-0.85, (1.0, 1.0, 1.0))
scene.set_background_color((0.5, 0.5, 0.4))
scene.set_directional_light((1, 5, 10), 0.2, (1, 0.8, 0.6))

@ti.func
def create_block(pos, size, color, color_noise):
    for I in ti.grouped(
            ti.ndrange((pos[0], pos[0] + size[0]), (pos[1], pos[1] + size[1]),
                       (pos[2], pos[2] + size[2]))):
        scene.set_voxel(I, 1, color + color_noise * ti.random())

@ti.func
def create_cut_ball(pos, size, color, color_noise) :
    r = size
    for x in range(-r,r) :
        for y in range(-r,r) :
            z2 = r*r-x*x-y*y
            if z2 < 0 :
                continue
            z = ti.sqrt(z2)

            i,j,k=0.0,0.0,0.0

            if x > 0 and y > 0 and z > 0 :
                pass
            else :
                i,j,k = x+pos.x,y+pos.y,z+pos.z
                create_block(ivec3(i, j, k), ivec3(1, 1, 1), color, color_noise)
                i,j,k = x+pos.x,z+pos.y,y+pos.z
                create_block(ivec3(i, j, k), ivec3(1, 1, 1), color, color_noise)
                i,j,k = z+pos.x,y+pos.y,x+pos.z
                create_block(ivec3(i, j, k), ivec3(1, 1, 1), color, color_noise)

            if z == 0 :
                continue
            if x > 0 and y > 0 and -z > 0 :
                continue
            z = -z

            i,j,k = x+pos.x,y+pos.y,z+pos.z
            create_block(ivec3(i, j, k), ivec3(1, 1, 1), color, color_noise)
            i,j,k = x+pos.x,z+pos.y,y+pos.z
            create_block(ivec3(i, j, k), ivec3(1, 1, 1), color, color_noise)
            i,j,k = z+pos.x,y+pos.y,x+pos.z
            create_block(ivec3(i, j, k), ivec3(1, 1, 1), color, color_noise)

@ti.kernel
def initialize_voxels():

    for r in range(1,9) :
        c1 = vec3(1.0, 0.0, 0.5)
        c2 = vec3(0.5, 1.0, 0.0)
        c3 = vec3(0.0, 0.5, 1.0)

        rnd = (r+1) % 3

        color = c1
        if rnd == 1 :
            color = c2
        elif rnd == 2 :
            color = c3
            
        create_cut_ball(
                ivec3(-10, -10, -10),
                ti.floor(40 * ti.pow(0.92,(r-1)*3))  - 0.5, 
                color, 
                vec3(0.10)
        )

initialize_voxels()

scene.finish()
