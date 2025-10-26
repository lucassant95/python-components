"""Tests for the System class."""

import pytest
from python_components.component import Component
from python_components.system import System


class MockLifecycleComponent(Component):
    """A mock component that tracks its lifecycle."""

    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.started = False
        self.shutdown_called = False
        self.start_order = None
        self.shutdown_order = None

    def start(self, system: Component):
        self.started = True

    def shutdown(self):
        self.shutdown_called = True

    def __repr__(self):
        return f"MockLifecycleComponent({self.name})"


def test_system_initialization():
    """Test that a system can be initialized with a component map."""
    comp1 = MockLifecycleComponent("comp1")
    system_map = {"comp1": comp1}

    system = System(system_map)
    assert system.state == "INITIALIZED"
    assert system.system_map == system_map


def test_system_starts_components():
    """Test that system.start() calls start on all components."""
    comp1 = MockLifecycleComponent("comp1")
    comp2 = MockLifecycleComponent("comp2")

    system_map = {"comp1": comp1, "comp2": comp2}
    system = System(system_map)

    system.start(system)

    assert comp1.started is True
    assert comp2.started is True
    assert system.state == "STARTED"


def test_system_shuts_down_components():
    """Test that system.shutdown() calls shutdown on all components."""
    comp1 = MockLifecycleComponent("comp1")
    comp2 = MockLifecycleComponent("comp2")

    system_map = {"comp1": comp1, "comp2": comp2}
    system = System(system_map)

    system.start(system)
    system.shutdown()

    assert comp1.shutdown_called is True
    assert comp2.shutdown_called is True
    assert system.state == "TERMINATED"


def test_system_dependency_order():
    """Test that components are started in dependency order."""
    start_sequence = []

    class OrderedComponent(Component):
        def __init__(self, name: str):
            super().__init__()
            self.name = name

        def start(self, system: Component):
            start_sequence.append(self.name)

        def shutdown(self):
            pass

    comp1 = OrderedComponent("comp1")
    comp2 = OrderedComponent("comp2").using(["comp1"])
    comp3 = OrderedComponent("comp3").using(["comp1"])
    comp4 = OrderedComponent("comp4").using(["comp2", "comp3"])

    system_map = {
        "comp1": comp1,
        "comp2": comp2,
        "comp3": comp3,
        "comp4": comp4,
    }

    system = System(system_map)
    system.start(system)

    # comp1 should start first (no dependencies)
    assert start_sequence[0] == "comp1"

    # comp2 and comp3 should start after comp1
    assert "comp2" in start_sequence[1:3]
    assert "comp3" in start_sequence[1:3]

    # comp4 should start last (depends on comp2 and comp3)
    assert start_sequence[3] == "comp4"


def test_system_shutdown_reverse_order():
    """Test that components are shut down in reverse dependency order."""
    shutdown_sequence = []

    class OrderedComponent(Component):
        def __init__(self, name: str):
            super().__init__()
            self.name = name

        def start(self, system: System):
            pass

        def shutdown(self):
            shutdown_sequence.append(self.name)

    comp1 = OrderedComponent("comp1")
    comp2 = OrderedComponent("comp2").using(["comp1"])
    comp3 = OrderedComponent("comp3").using(["comp2"])

    system_map = {
        "comp1": comp1,
        "comp2": comp2,
        "comp3": comp3,
    }

    system = System(system_map)
    system.start(system)
    system.shutdown()

    # Shutdown should be in reverse order: comp3 -> comp2 -> comp1
    assert shutdown_sequence == ["comp3", "comp2", "comp1"]


def test_system_missing_dependency():
    """Test that missing dependencies raise a KeyError."""
    comp1 = MockLifecycleComponent("comp1").using(["nonexistent"])

    system_map = {"comp1": comp1}
    system = System(system_map)

    with pytest.raises(KeyError, match="Component dependency 'nonexistent' not found"):
        system.start(system)


def test_system_circular_dependency():
    """Test that circular dependencies are detected."""
    # This would require modifying the system_map after component creation
    # to create a circular dependency
    comp1 = MockLifecycleComponent("comp1")
    comp2 = MockLifecycleComponent("comp2")

    # Create circular dependency manually
    comp1.dependencies = ["comp2"]
    comp2.dependencies = ["comp1"]

    system_map = {"comp1": comp1, "comp2": comp2}
    system = System(system_map)

    with pytest.raises(ValueError, match="Dependency graph has cycles"):
        system.start(system)


def test_system_complex_dependency_graph():
    """Test a more complex dependency graph."""
    # Create a diamond dependency pattern:
    #     comp1
    #    /     \
    # comp2   comp3
    #    \     /
    #     comp4

    comp1 = MockLifecycleComponent("comp1")
    comp2 = MockLifecycleComponent("comp2").using(["comp1"])
    comp3 = MockLifecycleComponent("comp3").using(["comp1"])
    comp4 = MockLifecycleComponent("comp4").using(["comp2", "comp3"])

    system_map = {
        "comp1": comp1,
        "comp2": comp2,
        "comp3": comp3,
        "comp4": comp4,
    }

    system = System(system_map)
    system.start(system)

    # All components should be started
    assert all(comp.started for comp in [comp1, comp2, comp3, comp4])

    system.shutdown()

    # All components should be shut down
    assert all(comp.shutdown_called for comp in [comp1, comp2, comp3, comp4])
