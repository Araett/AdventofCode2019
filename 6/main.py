
class Node:

    def __init__(self, name):
        self.name = name
        self.orbits = []
        self.distance_to_root = float('inf')
        self.predecessor = None

    def is_orbited_by(self, node):
        self.orbits.append(node)


def read_input():
    with open('input', 'r') as f:
        return f.readlines()


def parse_graph(unparsed_input):
    orbit_relations = []
    node_set = set()
    for relation in unparsed_input:
        node1, node2 = relation.split(')')
        node_set.add(node1)
        node_set.add(node2.rstrip())
        orbit_relations.append((node1, node2.rstrip()))
    return node_set, orbit_relations


def generate_vertices(vertices_names):
    vertices = {}
    for vertex in vertices_names:
        vertices[vertex] = Node(vertex)
    return vertices


def connect_vertices(relations, vertices):
    for relation in relations:
        vertices[relation[0]].is_orbited_by(vertices[relation[1]])


def relax(vertex1, vertex2):
    if (vertex1.distance_to_root + 1) < vertex2.distance_to_root:
        vertex2.distance_to_root = vertex1.distance_to_root + 1


def bellam_ford(root, vertices):
    root.distance_to_root = 0
    for i in range(1, len(vertices)):
        for _, vertex in vertices.items():
            for adj_vertex in vertex.orbits:
                relax(vertex, adj_vertex)
                adj_vertex.predecessor = vertex


def get_path_to_com(vertex):
    path = []
    current = vertex
    while current.name != 'COM':
        path.append(current.name)
        current = current.predecessor
    return path


def shortest_path(matrix, i, j, k):
    if matrix[(i, j)] > matrix[(i, k)] + matrix[(k, j)]:
        matrix[(i, j)] = matrix[(i, k)] + matrix[(k, j)]


# YEAH NO, O(n^3) SUCKS
def floyd_warshall(verticies):
    matrix = {}
    vertex_name_list = verticies.keys()
    all_conn = [(x, y) for x in vertex_name_list for y in vertex_name_list]
    for conn in all_conn:
        matrix[conn] = float('inf')
    for vertex_name in vertex_name_list:
        matrix[(vertex_name, vertex_name)] = 0
    for _, vertex in verticies.items():
        for adj_vertex in vertex.orbits:
            matrix[(vertex.name, adj_vertex.name)] = 1
            matrix[(adj_vertex.name, vertex.name)] = 1
    n = 0
    for i in vertex_name_list:
        n += 1
        print(f"{n} out of {len(vertex_name_list)}")
        for j in vertex_name_list:
            for k in vertex_name_list:
                shortest_path(matrix, i, j, k)
                if matrix[('YOU', 'SAN')] < float('inf'):
                    return matrix
    return matrix


def sum_all_orbits(vertices):
    total = 0
    for _, vertex in vertices.items():
        total += vertex.distance_to_root
    return total


def find_common_path(your_path, santa_path):
    print(your_path)
    print(santa_path)
    for i in range(1, len(your_path)):
        index = -1 * i
        print(your_path[index], santa_path[index])
        if your_path[-1 * i] != santa_path[-1 * i]:
            return your_path[-1*i:]
    return []


def main():
    unparsed_input = read_input()
    vertices_names, relations = parse_graph(unparsed_input)
    vertices = generate_vertices(vertices_names)
    connect_vertices(relations, vertices)
    root = vertices['COM']
    bellam_ford(root, vertices)
    your_path = get_path_to_com(vertices['YOU'])
    santa_path = get_path_to_com(vertices['SAN'])
    common_path_length = len(find_common_path(your_path, santa_path))
    print(len(your_path) + len(santa_path) - 2*common_path_length)


if __name__ == '__main__':
    main()
