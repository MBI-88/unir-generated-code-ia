# run-tests.ps1
Write-Host "=== Running tests with pytest on Windows PowerShell ==="

# Ejecutar pytest con cobertura
pytest --cov=src --cov=app -v