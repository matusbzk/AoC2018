import re
from collections import defaultdict
from copy import deepcopy


regex = re.compile(r'Step (\w) must be finished before step (\w) can begin.')
WORKERS = 5
STEP_DURATION_CONSTANT = 60


def get_processing_time(vertex):
    return STEP_DURATION_CONSTANT + 1 + ord(vertex) - ord('A')


class Graph:
    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges
        self.processing_vertices = defaultdict(int)
        self.free_workers = WORKERS

    def vertices_with_indegree_0(self):
        """Returns a set of vertices which do have in-degree 0."""
        result = set(self.vertices)
        for u, vs in self.edges.items():
            for v in vs:
                if v in result:
                    result.remove(v)
        return sorted(result)

    def remove_vertex_with_indegree_0(self, vertex):
        """Removes a vertex from the graph. Only works for vertices of indegree 0."""
        if vertex in self.processing_vertices:
            self.processing_vertices.remove(vertex)
        if vertex in self.vertices:
            self.vertices.remove(vertex)
            if vertex in self.edges:
                self.edges.pop(vertex)

    def vertices_that_can_be_processed(self):
        result = self.vertices_with_indegree_0()
        for v in self.processing_vertices:
            if v in result:
                result.remove(v)
        return result

    def process_vertex(self, vertex):
        if self.free_workers <= 0:
            raise ValueError("No free worker to process vertex " + vertex)
        self.free_workers -= 1
        self.processing_vertices[vertex] = get_processing_time(vertex)

    def next_step_in(self):
        to_process = self.vertices_that_can_be_processed()
        if self.free_workers > 0 and len(to_process) > 0:
            return 0
        if len(self.processing_vertices) == 0:
            return 99999999
        result = min(self.processing_vertices.values())
        return result

    def do_next_step(self, time=None):
        if time is None:
            time = self.next_step_in()
        if time == 0:
            vertex = graph.vertices_that_can_be_processed()[0]
            graph.process_vertex(vertex)
        else:
            to_delete = []
            for vertex, remaining in self.processing_vertices.items():
                if remaining == time:
                    to_delete.append(vertex)
                else:
                    self.processing_vertices[vertex] = remaining - time
            for vertex in to_delete:
                self.processing_vertices.pop(vertex)
                self.free_workers += 1
                self.remove_vertex_with_indegree_0(vertex)


def load_input():
    vertices = set([])
    edges = defaultdict(list)
    with open("input.txt", "r") as puzzle_input:
        for line in puzzle_input:
            matched = regex.match(line)
            u = matched.group(1)
            v = matched.group(2)
            vertices.add(u)
            vertices.add(v)
            edges[u].append(v)
    return Graph(vertices, edges)


def find_order(graph: Graph):
    order = ""
    while len(graph.vertices) > 0:
        vertex = graph.vertices_with_indegree_0()[0]
        order += vertex
        graph.remove_vertex_with_indegree_0(vertex)
    return order


def get_time_with_helpers(graph: Graph):
    time = 0
    while len(graph.vertices) > 0:
        step_in = graph.next_step_in()
        time += step_in
        graph.do_next_step(step_in)
    return time


graph = load_input()

graph_1 = deepcopy(graph)

print(find_order(graph_1))  # part 1

print(get_time_with_helpers(graph))  # part 2
