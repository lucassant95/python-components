# Python Components

A lightweight Python framework for managing the lifecycle and dependencies of stateful components.

Inspired by Alexandra Sierra's [Component](https://github.com/stuartsierra/component/) library for Clojure.

## Overview

**Component** is a small framework for managing the lifecycle of software components that have runtime state. It provides:

- **Dependency injection** using explicit dependency declarations
- **Lifecycle management** with `start` and `shutdown` methods
- **Automatic dependency resolution** using topological sorting
- **Clean separation** between component definition and composition

## Installation

```bash
uv add python-components
```

Or with pip:

```bash
pip install python-components
```

## Quick Start

### 1. Define Your Components

```python
from src.component import Component

class Database(Component):
    def __init__(self, host: str, port: int):
        super().__init__()
        self.host = host
        self.port = port
        self.connection = None
    
    def start(self):
        """Connect to the database."""
        self.connection = connect_to_db(self.host, self.port)
        print(f"Database connected to {self.host}:{self.port}")
    
    def shutdown(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            print("Database connection closed")

class WebServer(Component):
    def __init__(self, port: int):
        super().__init__()
        self.port = port
        self.server = None
    
    def start(self):
        """Start the web server."""
        self.server = start_server(self.port)
        print(f"Web server started on port {self.port}")
    
    def shutdown(self):
        """Stop the web server."""
        if self.server:
            self.server.stop()
            print("Web server stopped")
```

### 2. Compose Your System

```python
from src.system import System

# Build the system
system_map = {
    "database": Database(host="localhost", port=5432),
    "cache": Cache().using(["database"]),
    "web_server": WebServer(port=8080).using(["database", "cache"]),
}

system = System(system_map)
```

### 3. Start and Stop the System

```python
# Start all components in dependency order
system.start()

# Your application runs...

# Shutdown all components in reverse dependency order
system.shutdown()
```

## Key Concepts

### Components

A **component** is any object that:
- Extends the `Component` abstract base class
- Implements `start()` and `shutdown()` methods
- May depend on other components

### Dependencies

Declare dependencies using the `using()` method:

```python
component = MyComponent().using(["dependency1", "dependency2"])
```

Dependencies are automatically resolved and components are started in the correct order.

### System

A **system** is a collection of components with declared dependencies. The `System` class:
- Builds a dependency graph from component declarations
- Performs topological sorting to determine initialization order
- Starts components in dependency order
- Shuts down components in reverse dependency order
- Detects circular dependencies and raises an error

## Example: Complete Application

```python
from src.component import Component
from src.system import System

class Database(Component):
    def __init__(self, connection_string: str):
        super().__init__()
        self.connection_string = connection_string
        self.connection = None
    
    def start(self):
        self.connection = create_connection(self.connection_string)
        print("✓ Database connected")
    
    def shutdown(self):
        self.connection.close()
        print("✓ Database disconnected")

class Cache(Component):
    def __init__(self):
        super().__init__()
        self.data = {}
    
    def start(self):
        print("✓ Cache initialized")
    
    def shutdown(self):
        self.data.clear()
        print("✓ Cache cleared")

class ApiService(Component):
    def __init__(self):
        super().__init__()
        self.server = None
    
    def start(self):
        self.server = start_api_server()
        print("✓ API service started")
    
    def shutdown(self):
        self.server.stop()
        print("✓ API service stopped")

# Compose the system
system = System({
    "database": Database("postgresql://localhost/mydb"),
    "cache": Cache().using(["database"]),
    "api": ApiService().using(["database", "cache"]),
})

# Lifecycle management
try:
    system.start()
    # Application logic here
finally:
    system.shutdown()
```

## Features

- ✨ **Simple API**: Just implement `start()` and `shutdown()`
- 🔗 **Explicit Dependencies**: Clear, declarative dependency management
- 📊 **Automatic Ordering**: Topological sorting ensures correct initialization order
- 🔄 **Lifecycle Management**: Consistent start/shutdown across all components
- 🚨 **Cycle Detection**: Catches circular dependencies at runtime
- 🐍 **Pythonic**: Uses type hints and follows Python best practices

## Why Use Components?

### Problem: Global State and Initialization Order

Without a component system, applications often struggle with:
- Global mutable state scattered throughout the codebase
- Unclear initialization order leading to subtle bugs
- Difficulty testing components in isolation
- Complex shutdown logic that's easy to forget

### Solution: Managed Components

The Component pattern provides:
- **Explicit lifecycle**: Every stateful resource has clear start/shutdown methods
- **Dependency injection**: Components receive their dependencies explicitly
- **Testability**: Easy to create test doubles and inject them
- **Reliability**: Guaranteed correct initialization and cleanup order

## Development

### Running Tests

This project uses pytest for testing. To run the tests:

```bash
uv run pytest
```

To run tests with coverage:

```bash
uv run pytest --cov=src --cov-report=term-missing
```

### Installing Development Dependencies

```bash
uv add pytest ruff --group=dev
```

## Requirements

- Python >= 3.13
- networkx >= 3.5

## License

MIT License - see LICENSE file for details

## Acknowledgments

This library is inspired by Alexandra Sierra's [Component](https://github.com/stuartsierra/component/) library for Clojure, which pioneered the pattern of explicit lifecycle management and dependency injection using immutable data structures.

