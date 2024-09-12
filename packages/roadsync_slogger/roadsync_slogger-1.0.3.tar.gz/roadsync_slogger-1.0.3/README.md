# Roadsync SLogger

**Roadsync SLogger** is a Python logging library built to incorporate context enrichment like Go's slog module.

## Features

- Supports plain text and JSON logging formats.
- Allows dynamic context enrichment using `with_fields()`.
- Works seamlessly with Python's standard `logging` module.
- Handles complex and edge cases (e.g., empty messages, large log entries).
- Thread-safe with isolated logger instances.

## Installation

You can install **SLogger** from PyPI (once published) using `pip`:

```bash
pip install roadsync-slogger