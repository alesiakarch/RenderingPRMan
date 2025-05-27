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
print(f"verts_indices: {verts_indices}")

# Begin writing the object
ri.Begin("D20_subdiv.rib")

ri.Attribute("displacementbound", {"float sphere": 0.5, "string coordinatesystem": "object"})

# Optional: apply a transform so the object is positioned well
ri.TransformBegin()
ri.Scale(0.5, 0.5, 0.5)
ri.Rotate(20, 0, 1, 0)

# Flatten the list of vertices
points = [coord for v in vertices for coord in v]

# Create identical UVs for all faces
st = []
for face in faces:
    st.extend([0.0, 0.0])
    st.extend([1.0, 0.0]) 
    st.extend([0.5, 1.0])


# Each face has 3 vertices
nverts = [3] * len(faces)
verts = [i for face in faces for i in face]

print(f"ST: {st}")
print(f"len(vertices): {len(vertices)}")
print(f"len(st): {len(st)}")

uvs = []
for x, y, z in vertices:
    length = math.sqrt(x*x + y*y + z*z)
    nx, ny, nz = x / length, y / length, z / length

    u = 0.5 + (math.atan2(nz, nx) / (2 * math.pi))
    v = 0.5 - (math.asin(ny) / math.pi)

    uvs.extend([u, v])  # Flattened list of floats

print("UVs:", uvs)
print("Length of UV list:", len(uvs))

nfaces = 20
# Build facevarying face_id (3 entries per face)
face_ids = []
for i in range(nfaces):
    face_ids.extend([float(i)] * 3)  # One per corner of triangle

# Step 1: Build a set of unique undirected edges
# edges = set()  # Set ensures uniqueness of edges
# for face in faces:
#     for i in range(len(face)):
#         v0 = face[i]
#         v1 = face[(i + 1) % len(face)]  # Wraps around to close the loop
#         edge = tuple(sorted([v0, v1]))  # Sort to ensure undirected edges
#         edges.add(edge)

# Step 2: Convert edges into crease data
intargs = []
nargs = []
floatargs = []

# Step 2: Convert the edges into a flat list of integers (intargs)
edges = set()  # Use a set to store unique edges
for face in faces:
    v0, v1, v2 = face
    # Create edges for each triangle, and sort the vertex pairs to ensure uniqueness
    edges.add(tuple(sorted([v0, v1])))  # Edge between v0 and v1
    edges.add(tuple(sorted([v1, v2])))  # Edge between v1 and v2
    edges.add(tuple(sorted([v2, v0])))  # Edge between v2 and v0

print(f"{edges}")
#intargs = list(edges)
# for edge in edges:
#     # Edge already sorted, just add to intargs
#     intargs.extend(edge)  # Add the vertices of the edge
# for face in faces:
#     v0, v1, v2 = face
#     intargs.extend([v0, v1, v1, v2, v2, v0])  # Create edges for each triangle

#print(edges)

# Convert edges to flattened list
intargs = [v for edge in edges for v in edge] 

nargs = [2] * len(edges) * 2     # ONE entry: total number of ints
floatargs = [3.0] * 60
#face_ids = list(range(1, 21))  # [0, 1, 2, ..., 19]

face_pattern = [1, 19, 9, 11, 13, 7, 5, 15, 20, 8, 6, 16, 14, 12, 10, 2, 3, 4, 17, 18]  # correct order of number to map to face order 1 2 3 4 5 ... 20 
facevarying_faceid = []

for i in face_pattern:
    facevarying_faceid.extend([i, i, i])

#print("nargs:", nargs)
print("len(nargs):", len(nargs))
print("len(intargs):", len(intargs))
#print("intargs:", intargs)
print("len(floatargs):", len(floatargs))

# Now create the subdiv mesh
ri.SubdivisionMesh(
    "loop",           # No smoothing
    nverts,
    verts,
    [ri.CREASE] * len(edges),
    nargs,
    intargs,
    floatargs,
    {"P": points, 
     "facevarying float[2] st": st,
     "facevarying float faceid" : facevarying_faceid}  #"facevarying float face_id": face_ids
)

ri.TransformEnd()
ri.End()