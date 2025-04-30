#!/usr/bin/env prman.py
import prman 
import math

ri = prman.Ri()  # create an instance of the RenderMan interface
ri.Option("rib", {"string asciistyle": "indented"})

filename = "D12.rib"
# this is the begining of the rib archive generation we can only
# make RI calls after this function else we get a core dump
ri.Begin("__render")

# now we add the display element using the usual elements
# FILENAME DISPLAY Type Output format
ri.Display("D12.exr", "it", "rgba")
# Specify PAL resolution 1:1 pixel Aspect ratio
ri.Format(720, 575, 1)
# now set the projection to perspective
ri.Projection(ri.PERSPECTIVE, {ri.FOV: 50})
ri.Translate(0, 0, 5)  # move the camera back a bit

p = (1 + math.sqrt(5)) / 2


# Vertices for a dodecahedron (20 total)
vertices = [ (0, 1 / p, p), (0, -1 / p, p), (1, 1, 1),
            (-1, 1, 1), (-1, -1, 1), (1, -1, 1),
            (p, 0, 1 / p), (-p, 0, 1 / p), (1 / p, p, 0),
            (-1 / p, p, 0), (-1 / p, -p, 0), (1 / p, -p, 0),
            (p, 0, -1 / p), (-p, 0, -1 / p), (1, 1, -1),
            (-1, 1, -1), (-1, -1, -1), (1, -1, -1),
            (0, 1 / p, -p), (0, -1 / p, -p)]

# Faces of the dodecahedron (5 vertices per face) 
faces = [[0, 1, 5, 6, 2],
         [0, 1, 4, 7, 3],
         [0, 2, 8, 9, 3],
         [1, 5, 11, 10, 4],
         [5, 6, 12, 17, 11],
         [2, 8, 14, 12, 6],
         [4, 10, 16, 13, 7],
         [10, 11, 17, 19, 16],
         [3, 7, 13, 15, 9],
         [8, 9, 15, 18, 14],
         [12, 14, 18, 19, 17],
         [15, 13, 16, 19, 18]]


 
# Start the scene
ri.WorldBegin()

ri.Rotate(20, 1, 0, 0)  # Rotate the object to face the camera
for face in faces:
    points = []
    for i in face:
        points.append(vertices[i])  # Get the corresponding vertices
    
    # Flatten points for RIB and create the polygon
    flattened_points = []
    for pt in points:
        for p in pt:
            flattened_points.append(p)  # Flatten the list of points

    ri.Polygon({"P": flattened_points})  # Create the polygon with flattened points


ri.WorldEnd()