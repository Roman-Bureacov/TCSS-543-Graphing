"""Code for the generic graph data structure.

The purpose of this code is to create working code for graphs.
Contained is an abstract class for graphs, alongside a concrete
implementation being that of an adjacency list and an
adjacency matrix.

notation is: edges are (u, v) where an edge goes from u to v

"""

from abc import abstractmethod, ABC
from typing import override

class Node:
    """Basic representation of a node in a graph"""
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name
class Edge:
    def __init__(self, u: Node, v: Node, capacity: int):
        self.u = u
        self.v = v
        self.capacity = capacity
        self.flow = 0

from abc import abstractmethod, ABC
from typing import override

class Graph(ABC):
    """An abstract class for a network flow graph

    Network flow graphs are guaranteed to have no cycles.
    They have one source node s, and one sink node t.
    """

    source: Node
    sink: Node

    def __init__(self, source: Node, sink: Node):
        """Initialize the network flow graph

        Args:
            source: the flow source node
            sink: the flow sink node
        """
        self.source = source
        self.sink = sink
    
    @abstractmethod
    def adjacent_to(self, u: Node) -> list[Node]:
        """Returns the adjacent nodes
        
        Only returns nodes to which u can travel to.

        Args:
            u: the node to consider

        Returns:
            a list of nodes adjacent to u
        """
        raise NotImplementedError

    @abstractmethod
    def weight(self, u: Node, v: Node) -> int:
        """Return the capacity of the edge (u,v)

        Args:
            u: a node
            v: an adjacent node

        Returns:
            the capacity of the edge (u,v).

        Throws:
            ValueError: if the edge doesn't exist
        """
        raise NotImplementedError

    @abstractmethod
    def add_node(self, u: Node) -> None:
        """Add a node to the graph

        Args:
            u: a node
        """
        raise NotImplementedError

    @abstractmethod
    def remove_node(self, u: Node) -> None:
        """Remove a node from the graph

        Args:
            u: a node

        Throws:
            ValueError: if the node doesn't exist in the graph
        """
        raise NotImplementedError

    @abstractmethod
    def add_edge(self, u: Node, v: Node, weight: int) -> None:
        """Add an edge to the graph

        Args:
            u: a node
            v: a node
            weight: the edge weight

        Throws:
            ValueError: if the nodes don't exist in the graph
        """
        raise NotImplementedError

    @abstractmethod
    def remove_edge(self, u: Node, v: Node) -> None:
        """Remove an edge from the graph

        Args:
            u: a node
            v: a node

        Throws:
            ValueError: if the edge doesn't exist in the graph
        """
        raise NotImplementedError

    @abstractmethod
    def nodes(self) -> list[Node]:
        """Returns the list of nodes in this graph

        Returns:
            a list of nodes
        """
        raise NotImplementedError

    @abstractmethod
    def edges(self) -> list[tuple[Node, Node]]:
        """Returns the list of edges in this graph

        Returns:
            a list of edges
        """
        raise NotImplementedError

    @abstractmethod
    def __str__(self) -> str:
        """Return a string representation of the graph

        Returns:
            string representation of the graph
        """
        raise NotImplementedError

class ResidualGraph(Graph):
    """Creates a residual graph from an existing graph"""

    def __init__(self, graph):
        self.graph = graph
        self.residual_edges = {}

        self._add_residual_edges()
        
    def _add_residual_edges(self) -> None:
        """Adds residual edges to the graph
        """
        for e in self.graph.edges():
            u, v = e

            self.residual_edges[(u, v)] = 0
            self.residual_edges[(v, u)] = 0
            
    def add_flow(self, u: Node, v: Node, flow: int) -> None:
        """Add flow to an edge in the graph

        Args:
            u: a node
            v: a node
            flow: the flow to add

        """
        # TODO: bound?
        if flow > self.graph.weight(u, v): 
            raise ValueError("flow over capacity")
        
        self.residual_edges[(u, v)] += flow
        self.residual_edges[(v, u)] -= flow



class GraphAdjacencyList(Graph):
    """A graph represented by an adjacency list
    """

    def __init__(self, source: Node, sink: Node):
        super().__init__(source, sink)
        self.nodes: set[Node] = set() # nodes are held in a set
        self.edges: dict[Node, set[Node]] = {} # nodes mapped to other nodes they point to
        self.weights: dict[tuple[Node, Node], int] = {} # a lookup dictionary for edges

        self.nodes.add(source)
        self.nodes.add(sink)

    @override
    def adjacent_to(self, u: Node) -> list[Node]:
        return list(self.edges[u])

    @override
    def weight(self, u: Node, v: Node) -> int:
        return self.weights[(u, v)]

    @override
    def add_node(self, u: Node) -> None:
        self.nodes.add(u)
        self.edges[u] = set()

    @override
    def remove_node(self, u: Node) -> None:
        # remove all edges from nodes to this node
        for v in self.edges.keys():
            if u in self.edges[v]:
                self.edges[v].remove(u)
                self.weights.pop((v, u))
        # remove this node from adjacency list
        for v in self.edges[u]:
            self.weights.pop((u, v))
        self.edges.pop(u)
        # remove this node from nodes list
        self.nodes.remove(u)

    @override
    def add_edge(self, u: Node, v: Node, weight: int) -> None:
        k = self.edges.keys()
        if u not in k: raise ValueError("u is not a node in the graph")
        if v not in k: raise ValueError("v is not a node in the graph")
        e = (u, v)
        self.edges[u].add(v)
        self.weights[e] = weight

    @override
    def remove_edge(self, u: Node, v: Node):
        e = (u, v)
        self.edges[u].remove(v)
        self.weights.pop(e)

    @override
    def nodes(self) -> list[Node]:
        return list(self.nodes)

    @override
    def edges(self) -> list[tuple[Node, Node]]:
        r = []
        for (u, edges) in self.edges.items():
            for v in edges:
                r.append((u, v))
        return r

    @override
    def __str__(self) -> str:
        # make node string
        n = ""
        for node in self.nodes:
            n += f"{str(node)}, "
        n = n.rstrip(", ") # remove trailing ", "

        e = ""
        e_count = 0
        for u in self.edges.keys():
            for v in self.edges[u]:
                e_count += 1
                e += f"{str(u)} {str(v)} {self.weight(u, v)}\n"

        s = \
f"""
Nodes: {n}
{e_count} Edges:
(u, v, weight)
{e}
"""

        return s

class GraphAdjacencyMatrix(Graph):
    def __init__(self, source: Node, sink: Node, nodes: list[Node]):
        """initializes a graph represented by an adjacency matrix

        This graph does not permit a change in nodes, but allows for
        creation and deletion of edges.

        Args:
            source: the flow source node
            sink: the flow sink node
            nodes: the collection of all nodes in the graph

        """
        super().__init__(source, sink)
        # initialize the matrix to None (no edge)
        self.matrix: list[list[int | None]] = [
            [None for _ in range(len(nodes))]
            for _ in range(len(nodes))
        ] # mapping is: rows are u and columns are v

        # map nodes to an index
        self.indices: dict[Node, int] = {}
        for i, n in enumerate(nodes): self.indices[n] = i
        self.nodes = {n for n in nodes} # dupe the list into a set

    @override
    def adjacent_to(self, u: Node) -> list[Node]:
        pass

    @override
    def weight(self, u: Node, v: Node) -> int:
        r = self.matrix[self.indices[u]][self.indices[v]]
        if r is not None: return r
        else: raise ValueError("unknown edge u and v")

    @override
    def add_node(self, u: Node) -> None:
        raise NotImplementedError()

    @override
    def remove_node(self, u: Node) -> None:
        raise NotImplementedError()

    @override
    def add_edge(self, u: Node, v: Node, weight: int) -> None:
        self.matrix[self.indices[u]][self.indices[v]] = weight

    @override
    def remove_edge(self, u: Node, v: Node) -> None:
        self.matrix[self.indices[u]][self.indices[v]] = None

    @override
    def nodes(self) -> list[Node]:
        return list(self.nodes)

    @override
    def edges(self) -> list[tuple[Node, Node]]:
        l = []
        for u in self.indices.keys():
            for v in self.indices.keys():
                # index into the matrix, by getting the index of the nodes
                if self.matrix[self.indices[u]][self.indices[v]] is not None:
                    l.append((u, v))

        return l

    @override
    def __str__(self) -> str:

        # make node string
        n = ""
        for node in self.nodes:
            n += f"{str(node)}, "
        n = n.rstrip(", ")  # remove trailing ", "

        e = ""
        e_count = 0
        for u in self.indices.keys():
            for v in self.indices.keys():
                # index into the matrix, by getting the index of the nodes
                if self.matrix[self.indices[u]][self.indices[v]] is not None:
                    e_count += 1
                    e += f"{str(u)} {str(v)} {self.weight(u, v)}\n"

        s = \
f"""
Nodes: {n}
{e_count} Edges:
(u, v, weight)
{e}
"""

        return s