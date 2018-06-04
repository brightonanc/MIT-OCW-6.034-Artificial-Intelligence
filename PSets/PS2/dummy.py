# MY_CODE
# Just wanted a quick playground

def Dijkstra(graph, start, goal):
    Q = list(graph.nodes)
    dist = {start: 0}
    prev = {}

    # for each vertex v in Graph:             # Initialization
    #   dist[v] ← INFINITY                  # Unknown distance from source to v
    #   prev[v] ← UNDEFINED                 # Previous node in optimal path from source
    #   add v to Q                          # All nodes initially in Q (
    #   # unvisited nodes)

    while Q:
        node_to_extend = Q.pop(0)
        if node_to_extend == goal:
            # construct the path
            path = [goal]
            while path[0] != start:
                path.insert(0, prev[path[0]])
            return path
        for extension in graph.get_connected_nodes(node_to_extend):           # where v is still in Q.
            alt = dist[node_to_extend] + graph.get_edge(node_to_extend, extension).length
            if (extension not in dist) or (alt < dist[extension]):               # A shorter
                                                              # path to v has been found
                dist[extension] = alt
                prev[extension] = node_to_extend
        sort_key = lambda node: dist[node] if node in dist else 9999999
        Q.sort(key=sort_key)

    return []