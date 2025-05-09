#!/usr/bin/env prman.py
import prman
import math

ri = prman.Ri()
ri.Option("rib", {"string asciistyle": "indented"})

# Output and camera
ri.Display("D20.exr", "it", "rgba")
ri.Format(720, 575, 1)
ri.Projection(ri.PERSPECTIVE, {ri.FOV: 50})
ri.Translate(0, 0, 5)

# Golden ratio for d20 geometry
phi = (1 + math.sqrt(5)) / 2

# Unique vertex positions
vertices = [
    (0,  1,  phi), (0, -1,  phi), (0,  1, -phi), (0, -1, -phi),
    (1,  phi,  0), (-1,  phi, 0), (1, -phi, 0), (-1, -phi, 0),
    (phi, 0,  1), (-phi, 0, 1), (phi, 0, -1), (-phi, 0, -1)
]

# Triangle faces (indexing into vertices)
faces = [
    [0, 1, 8], [0, 8, 4], [0, 4, 5], [0, 5, 9], [0, 9, 1],
    [1, 6, 8], [1, 9, 7], [1, 7, 6],
    [2, 3, 11], [2, 10, 3], [2, 5, 4], [2, 4, 10], [2, 11, 5],
    [3, 6, 7], [3, 10, 6], [3, 7, 11],
    [4, 8, 10], [5, 11, 9], [6, 10, 8], [7, 9, 11]
]

# Convert vertex tuples to flat list
flat_verts = [coord for v in vertices for coord in v]

# Each triangle has 3 vertices
nverts = [3] * len(faces)

# Flatten face indices
verts_indices = [i for face in faces for i in face]

# Dummy UVs per vertex
st = []
for _ in vertices:
    st.extend([0.0, 0.0])  # You can later compute proper UVs if needed

# Begin writing the object
ri.Begin("../models/D20_subdiv.rib")

ri.Attribute("displacementbound", {"float sphere": 0.5, "string coordinatesystem": "object"})

# Optional: apply a transform so the object is positioned well
ri.TransformBegin()
ri.Scale(0.5, 0.5, 0.5)
ri.Rotate(20, 0, 1, 0)

# Flatten the list of vertices
points = [coord for v in vertices for coord in v]

# Create placeholder UVs (same layout repeated, not real unwrap)
st = []
for _ in range(len(vertices)):
    st.extend([0.5, 0.5])  # fake UVs for now

# Each face has 3 vertices
nverts = [3] * len(faces)
verts = [i for face in faces for i in face]

# ri.Attribute("subdivision", {
#     "string scheme": "bilinear",
#     "int dice:roundoff": [0],
#     "float dice:triangle": [0.1]  # finer subdivs = more geometry
# })

# Now create the subdiv mesh
ri.SubdivisionMesh(
    "bilinear",           # No smoothing
    nverts,
    verts,
    [], [], [], [],
    {"P": points, "st": st}
)

ri.TransformEnd()
ri.End()