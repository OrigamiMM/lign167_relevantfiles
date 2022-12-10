# simple version of height map generation from https://github.com/LoaDy588/py_terrain_mesh 

def generate_vertices_triangles(heightmap,MAP_SIZE):
    vertices = []
    base = (-1, -0.75, -1)
    size = 2
    max_height = 0.5
    step_x = size/(MAP_SIZE[0]-1)
    step_y = size/(MAP_SIZE[1]-1)

    for x in range(MAP_SIZE[0]):
        for y in range(MAP_SIZE[1]):
            x_coord = base[0] + step_x*x 
            y_coord = base[1] + max_height*heightmap[x][y]
            z_coord = base[2] + step_y*y
            vertices.append((x_coord, y_coord, z_coord))

    tris = []
    for x in range(MAP_SIZE[0]-1):
        for y in range(MAP_SIZE[1]-1):
            index = x*MAP_SIZE[0]+y
            a = index
            b = index+1
            c = index+MAP_SIZE[0]+1
            d = index+MAP_SIZE[0]
            tris.append((a, b, c))
            tris.append((a, c, d))

    return (vertices, tris)

def export_obj(vertices, tris, filename):
    file = open(filename, "w")
    for vertex in vertices:
      file.write("v " + str(vertex[0]) + " " + str(vertex[1]) + " " + str(vertex[2]) + "\n")
    for tri in tris:
      file.write("f " + str(tri[2]+1) + " " + str(tri[1]+1) + " " + str(tri[0]+1) + "\n")
    file.close()
    return

def generateOBJ(MAP_SIZE, MAP_norm, name):
    vertices, tris = generate_vertices_triangles(MAP_norm, MAP_SIZE)
    export_obj(vertices, tris, name)