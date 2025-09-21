#!/bin/bash
echo "=== Running tests with pytest on Unix/Linux ==="

# Ejecutar pytest con cobertura
pytest --cov=src --cov=app -v