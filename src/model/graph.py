from abc import abstractmethod, ABC

class Node:
    """Basic representation of a node in a graph"""
    def __init__(self, name):
        self.name = name


class Edge:
    def __init__(self, u: Node, v: Node, capacity: int):
        self.u = u
        self.v = v
        self.capacity = capacity
        self.flow = 0

class Graph(ABC):
    """An abstract class for a network flow graph

    Network flow graphs are guaranteed to have no cycles.
    They have one source node s, and one sink node t.
    """
    
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
    def add_edge(self, u: Node, v: Node, weight: int) -> None:
        """Add an edge to the graph

        Args:
            u: a node
            v: a node
            weight: the edge weight
        """
        raise NotImplementedError

    @abstractmethod
    def remove_edge(self, u: Node, v: Node):
        """Remove an edge from the graph

        Args:
            u: a node
            v: a node
        """
        raise NotImplementedError

    @abstractmethod
    def nodes(self) -> list[Node]:
        raise NotImplementedError

    @abstractmethod
    def edges(self) -> list[tuple[Node, Node]]:
        raise NotImplementedError

    @abstractmethod
    def to_string(self) -> str:
        """Return a string representation of the graph

        Returns:
            string representation of the graph
        """
        raise NotImplementedError

class ResidualGraph(Graph):
    """Creates a residual graph from an existing graph"""

    def __init__(self, graph):
        self.graph = graph
        self.forwardEdges = {}
        self.backwardEdges = {}

        self.add_residual_edges()
        
    def add_residual_edges(self):
        for e in self.graph.edges():
            u, v = e

            self.forwardEdges[(u, v)] = 0
            self.backwardEdges[(v, u)] = 0
            
    def add_flow(self, u, v, flow) -> None:
        # TODO: bound?
        if flow > self.graph.weight(u, v): 
            raise ValueError("flow over capacity")
        
        self.forwardEdges[(u, v)] += flow
        self.backwardEdges[(v, u)] -= flow

