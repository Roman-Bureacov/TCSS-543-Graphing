from controller.ScalingFulkerson import ScalingFulkerson


def main():
    graph = ScalingFulkerson()

    graph.add_edge("s", "A", 10)
    graph.add_edge("s", "B", 8)
    graph.add_edge("A", "B", 3)
    graph.add_edge("A", "t", 7)
    graph.add_edge("B", "t", 10)

    print(graph.to_string())

    # TODO: Execute max_flow()


if __name__ == "__main__":
    main()