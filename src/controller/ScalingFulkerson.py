
from model.graph import Graph, Node, Edge


class ScalingFulkerson(Graph):

    def __init__(self):
        # Hash maps to store forward and backward edges
        # Example: A ----10----> B
        # hashMap[A] = [Edge(A, B, 10)]  // forward A to B if (Key == A == Edge.u)
        # hashMap[B] = [Edge(A, B, 10)]  // backward B to A if (Key == B == Edge.v)
        self.adj: dict[Node, list[Edge]] = {}


    def add_edge(self, u: Node, v: Node, weight: int) -> None:
        if u not in self.adj:
            self.adj[u] = []

        if v not in self.adj:
            self.adj[v] = []

        edge = Edge(u, v, weight)

        # Both nodes reference the same Edge object
        self.adj[u].append(edge)
        self.adj[v].append(edge)

    def adjacent_to(self, u: Node) -> list[Node]:
        raise NotImplementedError

    def weight(self, u: Node, v: Node) -> int:
        raise NotImplementedError

    def nodes(self) -> list[Node]:
        raise NotImplementedError

    def edges(self) -> list[tuple[Node, Node]]:
        raise NotImplementedError

    def remove_edge(self, u: Node, v: Node):
        raise NotImplementedError

    def to_string(self) -> str:
        result = []

        for u in self.adj:
            result.append(f"Node {u}:")

            for edge in self.adj[u]:

                # Only print each original edge once
                if edge.u != u:
                    continue

                forward = edge.capacity - edge.flow
                backward = edge.flow

                result.append(
                    f"  {edge.u} -> {edge.v} | "
                    f"capacity={edge.capacity}, "
                    f"flow={edge.flow}, "
                    f"forward_residual={forward}, "
                    f"backward_residual={backward}"
                )

        return "\n".join(result)

    # ==============================
    # Scaling Ford-Fulkerson
    # ==============================

    def find_max_capacity(self) -> int:
        # TODO: Find maximum original edge capacity
        pass

    def find_augmenting_path(
        self, source: Node, sink: Node, delta: int
    ) -> list[tuple[Edge, bool]] | None:

        # TODO: find_augmenting_path
        pass

    def find_bottleneck(
        self, path: list[tuple[Edge, bool]]
    ) -> int:

        # TODO: find_bottleneck

        pass

    def augment_flow(
        self, path: list[tuple[Edge, bool]], bottleneck: int
    ) -> None:

        # TODO: augment_flow

        pass

    def max_flow(self, source: Node, sink: Node) -> int:

        # TODO: max_flow
        raise NotImplementedError
