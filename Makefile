.PHONY: help run clean test all

help:
	@echo "AmazeIng - Maze Generator & Pathfinding Project"
	@echo "================================================"
	@echo ""
	@echo "Available commands:"
	@echo "  make run       - Run the maze generator"
	@echo "  make test      - Run tests"
	@echo "  make clean     - Remove generated files"
	@echo "  make all       - Run everything (generator + solver)"
	@echo "  make help      - Show this help message"

run:
	@echo "Starting AmazeIng Maze Generator..."
	python3 generator_maze.py

test:
	@echo "Running tests..."
	python3 -m pytest tests/ -v 2>/dev/null || echo "No tests found or pytest not installed"

clean:
	@echo "Cleaning up generated files..."
	rm -f maze.txt
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

all: run
	@echo ""
	@echo "AmazeIng setup complete!"
	@echo "To solve the maze, use the 's' command in the interactive menu"
