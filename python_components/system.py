"""System class for managing component lifecycle and dependencies."""

from python_components.component import Component
from networkx import DiGraph, topological_sort, NetworkXUnfeasible


class System(Component):
    """A system manages the lifecycle of multiple components with dependencies."""

    def __init__(self, system_map: dict[str, Component]):
        super().__init__()
        self.system_map = system_map
        self.state: str = "INITIALIZED"

    def start(self, system: "System"):
        """Start all components in dependency order."""
        init_order = self.initialization_order()
        for component in init_order:
            component.start(self)
        self.state = "STARTED"

    def shutdown(self):
        """Shutdown all components in reverse dependency order."""
        init_order = self.initialization_order()
        init_order.reverse()
        for component in init_order:
            component.shutdown()
        self.state = "TERMINATED"

    def system_map_to_graph(self):
        """Convert the system map to a directed graph for dependency analysis."""
        graph = DiGraph()

        for component in self.system_map.values():
            graph.add_node(component)
            for dependency in component.dependencies:
                try:
                    component_dep = self.system_map[dependency]
                except KeyError as ke:
                    raise KeyError(
                        f"Component dependency '{dependency}' not found in system map"
                    ) from ke

                graph.add_edge(component, component_dep)
        return graph

    def initialization_order(self):
        """Determine the order in which components should be initialized."""
        graph = self.system_map_to_graph()
        try:
            components_list = list(topological_sort(graph))
            components_list.reverse()
            return components_list
        except NetworkXUnfeasible:
            raise ValueError(
                "Dependency graph has cycles; cannot determine initialization order."
            )

    def get_component(self, name: str) -> Component:
        """Retrieve a component by its name from the system map."""
        try:
            return self.system_map[name]
        except KeyError as ke:
            raise KeyError(f"Component '{name}' not found in system map") from ke


"""
Copyright (c) 2025 Lucas Sant'Anna

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
