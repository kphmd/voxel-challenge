from scene import Scene
import taichi as ti
from taichi.math import *

scene = Scene(voxel_edges=0, exposure=2)
scene.set_floor(-1.2, (1.0, 1.0, 1.0))
scene.set_background_color((0.5, 0.5, 0.4))
scene.set_directional_light((5, 15, 1), 0.1, (1.0, 1.0, 1.0))

@ti.func
def sdf(x,y,z) :
    res = 1
    r2 = x*x + y*y + z*z 
    r1 = ti.abs(x) + ti.abs(y) + ti.abs(z)
    r0 = (ti.max(ti.abs(x),ti.max(abs(y),abs(z))))

    if r0 >= 63 :
        res = 0

    a,b,c,d=50.0,50.0,50.0,50*1.73
    d2 = (x-a)**2 + (y-b)**2 + (z-c)**2
    if d2 <= d**2 :
        res = 0

    points = 0

    a,b,c,d=45.0,00.0,00.0,8.5
    d2x = (x-a)**2 + (y-b)**2 + (z-c)**2
    d2y = (x-b)**2 + (y-c)**2 + (z-a)**2
    d2z = (x-c)**2 + (y-a)**2 + (z-b)**2
    if d2x <= d**2 or d2y <= d**2 or d2z <= d**2 :
        points = 1

    a,b,c,d=30.0,30.0,-10.0,14.5
    d2x = (x-a)**2 + (y-b)**2 + (z-c)**2
    d2y = (x-b)**2 + (y-c)**2 + (z-a)**2
    d2z = (x-c)**2 + (y-a)**2 + (z-b)**2
    if d2x <= d**2 or d2y <= d**2 or d2z <= d**2 :
        points = 1

    balls = 0
    for i in range(1,9) :
        zoom = ti.pow(0.92,(i-1)*3)
        r = ti.floor(90 * zoom)  - 0.5
        if r2>=(r-2)**2 and r2<=r**2 :
            balls = 1
        
    res *= balls
    res += points
    return res

@ti.kernel
def initialize_voxels():

    for i in range(0,128**3) :
        x,y,z=i//(128**2)-64,(i//128)%128-64,i%128-64
        if 0==sdf(x,y,z) :
            continue
        scene.set_voxel(vec3(x,y,z),1,vec3(1.0-(x+64)/128,1.0-(z+64)/128,1.0-(y+64)/128))
        
initialize_voxels()

scene.finish()
