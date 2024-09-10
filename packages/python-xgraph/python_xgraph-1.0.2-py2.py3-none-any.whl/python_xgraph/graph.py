from collections import deque
from typing import List, Dict, Set, Optional, Any

"""
Graph Class

This class represents a graph data structure with functionalities to add vertices, add edges, remove vertices, remove edges, check for vertices and edges, perform traversals, check for cycles, perform topological sorting, and display the graph.

Attributes:
    graph (Dict[Any, List[Any]]): A dictionary representing the adjacency list of the graph.
    directed (bool): A flag indicating whether the graph is directed or not.

Methods:
    __init__(directed: bool = False):
        Initializes a new graph instance.

    add_vertex(vertex: Any) -> None:
        Adds a new vertex to the graph.

    add_edge(vertex1: Any, vertex2: Any) -> None:
        Adds an edge between two vertices.

    remove_vertex(vertex: Any) -> None:
        Removes a vertex and all its connected edges.

    remove_edge(vertex1: Any, vertex2: Any) -> None:
        Removes an edge between two vertices.

    has_vertex(vertex: Any) -> bool:
        Checks if a vertex is in the graph.

    has_edge(vertex1: Any, vertex2: Any) -> bool:
        Checks if an edge exists between two vertices.

    get_vertices() -> List[Any]:
        Returns a list of all vertices in the graph.

    get_edges() -> List[tuple]:
        Returns a list of all edges in the graph.

    dfs(start_vertex: Any) -> List[Any]:
        Performs Depth-First Search (DFS) starting from a given vertex.

    bfs(start_vertex: Any) -> List[Any]:
        Performs Breadth-First Search (BFS) starting from a given vertex.

    has_cycle() -> bool:
        Checks if the graph contains a cycle.

    topological_sort(reverse: bool = False) -> List[Any]:
        Performs topological sort on a directed graph and returns vertices in order.

    display() -> None:
        Displays the adjacency list of the graph.
"""
class Graph:
    def __init__(self, graph: dict = None, directed: bool = False):
        print(f"Initializing Graph with graph={graph}, directed={directed}")
        self.directed = directed
        self.graph = {}
        if graph is not None:
            self._init_graph(graph)
            self._validate_graph()

    def _init_graph(self, g: dict):
        if not isinstance(g, dict):
            raise ValueError("The graph must be a dictionary.")

        value_items = []
        for key in g.keys():
            value_items.append(key)
            
        for value in g.values():
            value_items.extend(value)
        
        value_items = list(set(value_items))
        
        for x in value_items:
            self.add_vertex(x)

        for key in g.keys():
            for item in g[key]:
                self.add_edge(key, item)
    
    def _validate_graph(self):
        """Validates that the input graph is correctly structured."""
        if not isinstance(self.graph, dict):
            raise ValueError("The graph must be a dictionary.")
        try:
            for vertex, neighbors in self.graph.items():
                
                for neighbor in neighbors:
                    # Ensure the neighbor is a valid vertex type
                    if not isinstance(neighbor, (str, int, float, tuple)):
                        raise ValueError(f"Invalid vertex type: '{neighbor}' in adjacency list of '{vertex}'.")

                    # If the graph is undirected, ensure symmetry
                    if not self.directed and neighbor in self.graph and vertex not in self.graph[neighbor]:
                        raise ValueError(f"Edge ({vertex}, {neighbor}) is not bidirectional in an undirected graph.")
        except Exception:
            raise ValueError(f"Edge ({vertex}, {neighbor}) is not properly defined for the graph.")

    def add_vertex(self, vertex: Any) -> None:
        """Adds a new vertex to the graph."""
        if vertex in self.graph:
            raise ValueError(f"Vertex '{vertex}' already exists.")
        self.graph[vertex] = []

    def add_edge(self, vertex1: Any, vertex2: Any) -> None:
        """Adds an edge between two vertices."""
        if vertex1 not in self.graph:
            self.add_vertex(vertex1)
        if vertex2 not in self.graph:
            self.add_vertex(vertex2)

        if vertex2 in self.graph[vertex1]:
            raise ValueError(f"Edge from '{vertex1}' to '{vertex2}' already exists.")

        self.graph[vertex1].append(vertex2)
        if not self.directed:
            self.graph[vertex2].append(vertex1)

    def remove_vertex(self, vertex: Any) -> None:
        """Removes a vertex and all its connected edges."""
        if vertex not in self.graph:
            raise ValueError(f"Vertex '{vertex}' does not exist.")

        # Remove all edges from this vertex
        for adj_vertex in list(self.graph[vertex]):
            self.remove_edge(vertex, adj_vertex)

        # Remove all edges to this vertex
        for v in self.graph:
            if vertex in self.graph[v]:
                self.graph[v].remove(vertex)

        del self.graph[vertex]

    def remove_edge(self, vertex1: Any, vertex2: Any) -> None:
        """Removes an edge between two vertices."""
        if vertex1 not in self.graph or vertex2 not in self.graph:
            raise ValueError("One or both vertices do not exist.")

        if vertex2 not in self.graph[vertex1]:
            raise ValueError(f"Edge from '{vertex1}' to '{vertex2}' does not exist.")
        
        self.graph[vertex1].remove(vertex2)
        if not self.directed:
            self.graph[vertex2].remove(vertex1)

    def has_vertex(self, vertex: Any) -> bool:
        """Checks if a vertex is in the graph."""
        return vertex in self.graph

    def has_edge(self, vertex1: Any, vertex2: Any) -> bool:
        """Checks if an edge exists between two vertices."""
        return vertex1 in self.graph and vertex2 in self.graph[vertex1]

    def get_vertices(self) -> List[Any]:
        """Returns a list of all vertices in the graph."""
        return list(self.graph.keys())

    def get_edges(self) -> List[tuple]:
        """Returns a list of all edges in the graph."""
        edges = []
        for vertex, neighbors in self.graph.items():
            for neighbor in neighbors:
                if self.directed or (neighbor, vertex) not in edges:
                    edges.append((vertex, neighbor))
        return edges

    def dfs(self, start_vertex: Any) -> List[Any]:
        """Performs Depth-First Search (DFS) starting from a given vertex."""
        visited = set()
        result = []

        def _dfs(vertex: Any):
            visited.add(vertex)
            result.append(vertex)
            for neighbor in self.graph[vertex]:
                if neighbor not in visited:
                    _dfs(neighbor)

        if start_vertex not in self.graph:
            raise ValueError(f"Start vertex '{start_vertex}' does not exist.")
        
        _dfs(start_vertex)
        return result

    def bfs(self, start_vertex: Any) -> List[Any]:
        """Performs Breadth-First Search (BFS) starting from a given vertex."""
        if start_vertex not in self.graph:
            raise ValueError(f"Start vertex '{start_vertex}' does not exist.")

        visited = set()
        queue = deque([start_vertex])
        result = []

        while queue:
            vertex = queue.popleft()
            if vertex not in visited:
                visited.add(vertex)
                result.append(vertex)
                queue.extend([neighbor for neighbor in self.graph[vertex] if neighbor not in visited])
        
        return result

    def has_cycle(self) -> bool:
        """Checks if the graph contains a cycle."""
        visited = set()

        def dfs(vertex: Any, parent: Optional[Any]) -> bool:
            visited.add(vertex)
            for neighbor in self.graph[vertex]:
                if neighbor not in visited:
                    if dfs(neighbor, vertex):
                        return True
                elif neighbor != parent:
                    return True
            return False

        def dfs_directed(vertex: Any, rec_stack: Set[Any]) -> bool:
            visited.add(vertex)
            rec_stack.add(vertex)

            for neighbor in self.graph[vertex]:
                if neighbor not in visited:
                    if dfs_directed(neighbor, rec_stack):
                        return True
                elif neighbor in rec_stack:
                    return True

            rec_stack.remove(vertex)
            return False

        if self.directed:
            rec_stack = set()
            for vertex in self.graph:
                if vertex not in visited:
                    if dfs_directed(vertex, rec_stack):
                        return True
        else:
            for vertex in self.graph:
                if vertex not in visited:
                    if dfs(vertex, None):
                        return True

        return False

    def topological_sort(self, reverse: bool = False) -> List[Any]:
        """Performs topological sort on a directed graph and returns vertices in order.
        If reverse is False, returns from parent to child; if True, returns from child to parent."""
        if not self.directed:
            raise ValueError("Topological sort is only applicable to directed graphs.")

        # Detect cycles before performing topological sort
        if self.has_cycle():
            raise ValueError("Graph has a cycle, topological sort is not possible.")

        visited = set()
        stack = []

        def dfs(vertex: Any):
            visited.add(vertex)
            for neighbor in self.graph[vertex]:
                if neighbor not in visited:
                    dfs(neighbor)
            stack.append(vertex)

        for vertex in self.graph:
            if vertex not in visited:
                dfs(vertex)

        return stack[::-1] if not reverse else stack


    def display(self) -> None:
        """Displays the adjacency list of the graph."""
        for vertex in self.topological_sort():
            neighbors = self.graph[vertex]
            if len(neighbors) > 0 :
                print(f"{vertex}: {neighbors}")
