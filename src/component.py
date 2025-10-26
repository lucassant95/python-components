"""Component base class for lifecycle management."""

from abc import ABC, abstractmethod
from typing import final


class Component(ABC):
    """Abstract base class for all components with lifecycle management.

    Components are objects that have runtime state and need explicit
    lifecycle management (start/shutdown). They can declare dependencies
    on other components using the using() method.
    """

    def __init__(self):
        """Initialize a component with an empty dependency list."""
        self.dependencies: list[str] = []

    @abstractmethod
    def start(self):
        """Connect to the component's resources.

        This method should initialize any runtime state, establish connections,
        open files, etc. It will be called after all dependencies have been started.
        """
        pass

    @abstractmethod
    def shutdown(self):
        """Gracefully disconnect from the component's resources.

        This method should clean up any runtime state, close connections,
        release resources, etc. It will be called before any dependencies are shut down.
        """
        pass

    @final
    def using(self, dependencies: list[str]) -> "Component":
        """Declare dependencies on other components.

        Args:
            dependencies: List of component names (keys in the system map)
                         that this component depends on.

        Returns:
            Self, to allow method chaining.

        Example:
            >>> cache = Cache().using(["database"])
            >>> api = ApiService().using(["database", "cache"])
        """
        self.dependencies = dependencies
        return self


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
