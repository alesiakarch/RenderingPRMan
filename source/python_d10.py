#!/usr/bin/env prman.py
import prman 
import math

ri = prman.Ri()  # create an instance of the RenderMan interface
ri.Option("rib", {"string asciistyle": "indented"})

filename = "D10.rib"
# this is the begining of the rib archive generation we can only
# make RI calls after this function else we get a core dump
ri.Begin("__render")

# now we add the display element using the usual elements
# FILENAME DISPLAY Type Output format
ri.Display("D10.exr", "it", "rgba")
# Specify PAL resolution 1:1 pixel Aspect ratio
ri.Format(720, 575, 1)
# now set the projection to perspective
ri.Projection(ri.PERSPECTIVE, {ri.FOV: 50})
ri.Translate(0, 0, 5)  # move the camera back a bit

# now we start our world
ri.WorldBegin()
# Geometry: D10
num_faces = 10
#top = 1
#bottom = -1
radius = 1
height_offset = 0.2  # slight vertical offset for kite shape
top = (0, 1, 0)
bottom = (0, -1, 0)
offset = 0.1
points = []
points = []

def flatten(p): 
    return [p[0], p[1], p[2]]
ri.Rotate(90, 0, 1, 0)  # Rotate the object to face the camera
# First loop: generate 10 alternating points around a circle
for i in range(num_faces):
    angle = i * 2 * math.pi / num_faces
    x = radius * math.cos(angle)
    z = radius * math.sin(angle)
    y = offset if i % 2 == 0 else -offset
    points.append((x, y, z))

# Second loop: generate faces between top/bottom and point pairs
j = 0
while j < num_faces:
    p1 = points[j]
    p2 = points[(j + 1) % num_faces]
    p3 = points[(j + 2) % num_faces]
    p4 = points[(j + 3) % num_faces]

    ri.Bxdf("PxrDiffuse", "diffuse", {"color diffuseColor": [1.0, 0.0, 1.0]})
    ri.Polygon({"P": flatten(top) + flatten(p1) + flatten(p2) + flatten(p3)})

    ri.Bxdf("PxrDiffuse", "diffuse2", {"color diffuseColor": [1.0, 1.0, 0.0]})
    ri.Polygon({"P": flatten(bottom) + flatten(p2) + flatten(p3) + flatten(p4)})

    j += 2  # Skip ahead by 2 to avoid reusing same points

ri.WorldEnd()