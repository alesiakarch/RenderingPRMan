#!/usr/bin/env prman.py
import prman 
import math
import random

ri = prman.Ri()  # create an instance of the RenderMan interface
ri.Option("rib", {"string asciistyle": "indented"})


filename = "D20.rib"
# this is the begining of the rib archive generation we can only
# make RI calls after this function else we get a core dump


# now we add the display element using the usual elements
# FILENAME DISPLAY Type Output format
ri.Display("D20.exr", "it", "rgba")
# Specify PAL resolution 1:1 pixel Aspect ratio
ri.Format(720, 575, 1)
# now set the projection to perspective
ri.Projection(ri.PERSPECTIVE, {ri.FOV: 50})
ri.Translate(0, 0, 5)  # move the camera back a bit

def flatten(p): 
    return [p[0], p[1], p[2]]

phi = (1 + math.sqrt(5)) / 2

vertices = [
    (0,  1,  phi),     # 0
    (0, -1,  phi),     # 1
    (0,  1, -phi),     # 2
    (0, -1, -phi),     # 3
    (1,  phi,  0),     # 4
    (-1,  phi, 0),     # 5
    (1, -phi, 0),      # 6
    (-1, -phi, 0),     # 7
    (phi, 0,  1),      # 8
    (-phi, 0, 1),      # 9
    (phi, 0, -1),      #10
    (-phi, 0, -1)      #11
]

faces = [
    [0, 1, 8],
    [0, 8, 4],
    [0, 4, 5],
    [0, 5, 9],
    [0, 9, 1],
    [1, 6, 8],
    [1, 9, 7],
    [1, 7, 6],
    [2, 3, 11],
    [2, 10, 3],
    [2, 5, 4],
    [2, 4, 10],
    [2, 11, 5],
    [3, 6, 7],
    [3, 10, 6],
    [3, 7, 11],
    [4, 8, 10],
    [5, 11, 9],
    [6, 10, 8],
    [7, 9, 11]
]
ri.Begin("../models/D20.rib")

for tri in faces:
    points = []
     # set the UV coordinates for the vertices
    st = [ 0.0, 0.0, 1.0, 0.0, 0.5, 1.0  ]
    for i in tri:
        points.extend(flatten(vertices[i]))  # Get the corresponding vertices

   
    
    #ri.Bxdf("PxrDiffuse", "diffuse", {"color diffuseColor": [random.random(), random.random(), random.random()]})
    ri.Polygon({"P": points, "st": st})  # Create the polygon with flattened points


ri.End()  # End the rib archive