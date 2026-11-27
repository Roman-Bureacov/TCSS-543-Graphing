"""Creation of graphs.

This file is associated with creation of graphs, and is dedicated
to the GraphFactory which will make random graphs as necessary.

Note that this is dedicated to making network flow graphs

"""
import random

from src.model.graph import Graph, GraphAdjacencyList, Node


class GraphFactory:
    """Factory class for creating network flow graphs.

    props:

    """

    r = random.Random()
    """The random device used by the graph factory"""

    def __init__(self):
        """Raises an exception

        This class is not to be instantiated and
        this function will raise an exception.

        Throws:
            RuntimeError: GraphFactory is a static class
        """
        raise RuntimeError('GraphFactory is a static class')

    @staticmethod
    def random_graph(n: int, p: float, max_weight: int = 1) -> Graph:
        """Creates a random graph

        Creates a random graph with n nodes. Edges are randomly weighted
        with uniform distribution, from and including 1 up to and including
        max_weight.

        Args:
            n: number of nodes in the graph (at least 2, the source and sink)
            p: probability of an edge between two nodes
            max_weight: maximum weight of any random edge in the graph, inclusive

        throws:
            ValueError
        """

        if n < 2: raise ValueError('n must be at least 2')
        s = Node("source")
        t = Node("sink")
        g = GraphAdjacencyList(s, t)

        nodes = [ Node(f"n{i}") for i in range(n - 2) ] # create the rest of the nodes
        nodes.insert(0, s)
        nodes.append(t)
        for n_i in nodes: g.add_node(n_i)

        # the method: you can only create edges that go from low to high, but not high to low
        for i in range(n):
            for j in range(i + 1, n):
                k = GraphFactory.r.randint(0, 100)
                if k/100.0 <= p:
                    g.add_edge(
                        nodes[i],
                        nodes[j],
                        GraphFactory.r.randint(1, max_weight)
                    )

        return g

    @staticmethod
    def mesh_graph(n: int) -> Graph:
        """Creates a mesh graph

        For further information on what a mesh graph is:
        https://en.wikipedia.org/wiki/Lattice_graph

        Args:
            n: number of nodes

        Returns:
            a mesh graph with n nodes
        """
        raise NotImplementedError

    @staticmethod
    def bipartite_graph(n: int) -> Graph:
        """Creates a bipartite graph

        Args:
            n: number of nodes
        """
        raise NotImplementedError

    @staticmethod
    def range_graph(n: int, min: int, max: int) -> Graph:
        """

        Args:
            n: the number of nodes
            min: the minimum for range
            max: the maximum for range

        Returns:
            a graph with n nodes
        """
        raise NotImplementedError

    @staticmethod
    def set_seed(seed: int) -> None:
        """Sets the seed for random graphs.

        Args:
            seed: seed for random graphs
        """
        GraphFactory.r.seed(seed)
