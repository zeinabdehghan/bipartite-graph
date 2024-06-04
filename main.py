import networkx as nx
import matplotlib.pyplot as plt

def read_file(file_path):
    graph = {}

    try:
        with open(file_path, 'r') as file:
            for line_number, line in enumerate(file, start=1):
                try:

                    vertices = [int(vertex) for vertex in line.strip('{} \n').split()]
                    u, v = vertices[0], vertices[1]
                except ValueError:
                    print(f"Error on line {line_number}: Invalid vertex format.")
                    continue

                if u not in graph:
                    graph[u] = []
                if v not in graph:
                    graph[v] = []

                graph[u].append(v)
                graph[v].append(u)

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
    print(graph)
    return graph

def dfs(graph):
    num_v = len(graph)
    colors = {}
    stack = []

    for v in range(num_v):
        if v in colors:
            continue

        stack.append((v, 0))

        while stack:
            current_v, color = stack.pop()

            if current_v in colors:
                if colors[current_v] != color:
                    print('DFS: No, the graph is not bipartite.')
                    return graph, False , colors
                continue

            colors[current_v] = color

            for neighbor in graph[current_v]:
                stack.append((neighbor, 1 - color))

    print('DFS: Yes, the graph is bipartite.')
    return graph, True, colors

def bfs(graph):
    colors = {}
    queue = []

    for v in graph:
        if v not in colors:
            queue.append(v)
            colors[v] = 0

            while queue:
                current_v = queue.pop(0)

                for n in graph[current_v]:
                    if n not in colors:
                        colors[n] = 1 - colors[current_v]
                        queue.append(n)
                    elif colors[n] == colors[current_v]:
                        print("BFS: No, the graph is not bipartite.")
                        return graph, False ,colors

    print("BFS: Yes, the graph is bipartite.")
    return graph, True, colors

def ids(graph):
    def dfs(v, color, d, colors):
        if v in colors:
            return colors[v] == color
        if d == 0:
            return True
        colors[v] = color
        return all(dfs(n, 1 - color, d - 1, colors) for n in graph[v])

    for d_limit in range(1, len(graph) + 1):
        colors = {}
        for v in graph:
            if v not in colors:
                if not dfs(v, 0, d_limit, colors):
                    break

        else:
            print(f"IDS: Yes, the graph is bipartite.")
            return graph, True, colors

    print(f"IDS: No, the graph is not bipartite.")
    return graph, False, colors

def visualize(graph_info):
    graph, is_bipartite, colors = graph_info

    if not is_bipartite:
        print("Nothing to show, graph is not bipartite.")
        return

    G = nx.Graph()

    for u, neighbors in graph.items():
        for v in neighbors:
            G.add_edge(u, v)

    pos = nx.shell_layout(G, nlist=[list(graph.keys())])


    node_colors = [colors[node] for node in G.nodes]


    red_nodes = [node for node, color in colors.items() if color == 0]
    blue_nodes = [node for node, color in colors.items() if color == 1]


    pos.update((node, (x, 1)) for x, node in enumerate(red_nodes, start=1))
    pos.update((node, (x, -1)) for x, node in enumerate(blue_nodes, start=1))


    nx.draw(G, pos, with_labels=True, node_color=node_colors, cmap=plt.cm.rainbow)


    plt.show()

file_path = "graph3.edgelist"

graph = read_file(file_path)

bfs_info = bfs(graph)
dfs_info = dfs(graph)
ids_info = ids(graph)

#use any info to visualize
visualize(bfs_info)