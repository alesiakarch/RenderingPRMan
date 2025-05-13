faces = [
    [0, 1, 8], [0, 8, 4], [0, 4, 5], [0, 5, 9], [0, 9, 1],
    [1, 6, 8], [1, 9, 7], [1, 7, 6],
    [2, 3, 11], [2, 10, 3], [2, 5, 4], [2, 4, 10], [2, 11, 5],
    [3, 6, 7], [3, 10, 6], [3, 7, 11],
    [4, 8, 10], [5, 11, 9], [6, 10, 8], [7, 9, 11]
]
# edges = []
# for face in faces:
#     v0, v1, v2 = face
#     edges.extend([v0, v1, v1, v2, v2, v0])  # Create edges for each triangle

# print(edges)

edges = set()  # Use a set to store unique edges
for face in faces:
    v0, v1, v2 = face
    # Create edges for each triangle, and sort the vertex pairs to ensure uniqueness
    edges.add(tuple(sorted([v0, v1])))  # Edge between v0 and v1
    edges.add(tuple(sorted([v1, v2])))  # Edge between v1 and v2
    edges.add(tuple(sorted([v2, v0])))  # Edge between v2 and v0

# Convert the set to a list if you need it in list form
edges = list(edges)

print(f"Total unique edges: {len(edges)}")
print(f"Edges: {edges}")