"""Tests for the Component class."""

from python_components.component import Component


class MockComponent(Component):
    """A mock component for testing."""

    def __init__(self):
        super().__init__()
        self.started = False
        self.shutdown_called = False

    def start(self):
        self.started = True

    def shutdown(self):
        self.shutdown_called = True


def test_component_initialization():
    """Test that a component can be initialized."""
    component = MockComponent()
    assert component.dependencies == []
    assert component.started is False
    assert component.shutdown_called is False


def test_component_using():
    """Test that dependencies can be declared using the using() method."""
    component = MockComponent().using(["dependency1", "dependency2"])
    assert component.dependencies == ["dependency1", "dependency2"]


def test_component_using_returns_self():
    """Test that using() returns the component instance for method chaining."""
    component = MockComponent()
    result = component.using(["dep1"])
    assert result is component


def test_component_lifecycle():
    """Test that start and shutdown methods can be called."""
    component = MockComponent()

    component.start()
    assert component.started is True

    component.shutdown()
    assert component.shutdown_called is True
