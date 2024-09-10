import sys
import os

from python_xgraph.graph import Graph
import unittest

class TestGraph(unittest.TestCase):

    def setUp(self):
        """Set up a basic graph for testing."""
        self.graph = Graph(directed=True)
        self.graph.add_vertex("A")
        self.graph.add_vertex("B")
        self.graph.add_vertex("C")
        self.graph.add_edge("A", "B")
        self.graph.add_edge("B", "C")

    def test_add_vertex(self):
        """Test adding a vertex."""
        self.graph.add_vertex("D")
        self.assertTrue(self.graph.has_vertex("D"))
        self.assertRaises(ValueError, self.graph.add_vertex, "A")

    def test_add_edge(self):
        """Test adding an edge."""
        self.graph.add_edge("C", "A")
        self.assertTrue(self.graph.has_edge("C", "A"))
        self.assertRaises(ValueError, self.graph.add_edge, "A", "B")

    def test_remove_vertex(self):
        """Test removing a vertex."""
        self.graph.remove_vertex("B")
        self.assertFalse(self.graph.has_vertex("B"))
        self.assertFalse(self.graph.has_edge("A", "B"))
        self.assertRaises(ValueError, self.graph.remove_vertex, "Z")

    def test_remove_edge(self):
        """Test removing an edge."""
        self.graph.remove_edge("A", "B")
        self.assertFalse(self.graph.has_edge("A", "B"))
        self.assertRaises(ValueError, self.graph.remove_edge, "A", "B")

    def test_dfs(self):
        """Test DFS traversal."""
        result = self.graph.dfs("A")
        self.assertEqual(result, ["A", "B", "C"])

    def test_bfs(self):
        """Test BFS traversal."""
        result = self.graph.bfs("A")
        self.assertEqual(result, ["A", "B", "C"])

    def test_has_cycle(self):
        """Test cycle detection."""
        self.assertFalse(self.graph.has_cycle())
        self.graph.add_edge("C", "A")
        self.assertTrue(self.graph.has_cycle())

    def test_topological_sort(self):
        """Test topological sort."""
        result = self.graph.topological_sort()
        self.assertEqual(result, ["A", "B", "C"])
        self.graph.add_edge("C", "A")
        self.assertRaises(ValueError, self.graph.topological_sort)

    def test_init_with_dict(self):
        """Test initializing a graph with a dictionary."""
        graph_dict = {"A": ["B", "C"], "B": ["C"], "C": []}
        graph = Graph(graph=graph_dict, directed=True)
        self.assertTrue(graph.has_vertex("A"))
        self.assertTrue(graph.has_vertex("B"))
        self.assertTrue(graph.has_vertex("C"))
        self.assertTrue(graph.has_edge("A", "B"))
        self.assertTrue(graph.has_edge("A", "C"))
        self.assertTrue(graph.has_edge("B", "C"))

    def test_get_vertices(self):
        """Test getting all vertices."""
        vertices = self.graph.get_vertices()
        self.assertEqual(set(vertices), {"A", "B", "C"})

    def test_get_edges(self):
        """Test getting all edges."""
        edges = self.graph.get_edges()
        self.assertEqual(set(edges), {("A", "B"), ("B", "C")})

    def test_undirected_graph(self):
        """Test undirected graph behavior."""
        undirected_graph = Graph(directed=False)
        undirected_graph.add_edge("X", "Y")
        self.assertTrue(undirected_graph.has_edge("X", "Y"))
        self.assertTrue(undirected_graph.has_edge("Y", "X"))

    def test_topological_sort_reverse(self):
        """Test topological sort with reverse option."""
        result = self.graph.topological_sort(reverse=True)
        self.assertEqual(result, ["C", "B", "A"])

    def test_display(self):
        """Test display method (this is more of a smoke test)."""
        # Redirect stdout to capture print output
        from io import StringIO
        import sys
        captured_output = StringIO()
        sys.stdout = captured_output
        self.graph.display()
        sys.stdout = sys.__stdout__
        self.assertIn("A: ['B']", captured_output.getvalue())
        self.assertIn("B: ['C']", captured_output.getvalue())

if __name__ == "__main__":
    unittest.main()
