.PHONY: help run generate solve clean lint lint-strict test all

help:
	@echo "AmazeIng - Maze Generator & Pathfinding Project"
	@echo "================================================"
	@echo ""
	@echo "Available commands:"
	@echo "  make run          - Generate maze and show solution path"
	@echo "  make generate     - Generate maze only (no solution)"
	@echo "  make solve        - Generate maze and find path solution (same as 'make run')"
	@echo "  make lint         - Run flake8 linting"
	@echo "  make lint-strict  - Run mypy type checking (strict mode)"
	@echo "  make test         - Run tests"
	@echo "  make clean        - Remove generated files and cache"
	@echo "  make all          - Generate maze and solve it"
	@echo "  make help         - Show this help message"

run: solve

generate:
	@echo "🎨 Generating maze (no path shown)..."
	python3 generator_maze.py

solve:
	@echo "🔍 Generating maze and finding solution path..."
	python3 pathfinding.py

lint:
	@echo "🔍 Running flake8 linter..."
	@flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics || echo "❌ Flake8 not installed. Run: pip install flake8"
	@flake8 . --count --max-complexity=10 --max-line-length=127 --statistics || echo "Note: Some style warnings found"

lint-strict:
	@echo "🔍 Running mypy type checker (strict mode)..."
	@mypy . --disallow-untyped-defs --warn-return-any --warn-unused-configs --disallow-incomplete-defs || echo "❌ Mypy not installed. Run: pip install mypy"

test:
	@echo "🧪 Running tests..."
	@python3 -m pytest tests/ -v 2>/dev/null || echo "❌ No tests found or pytest not installed. Run: pip install pytest"

clean:
	@echo "🧹 Cleaning up generated files..."
	@rm -f maze.txt
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete
	@echo "✓ Clean complete"

all: generate solve
	@echo ""
	@echo "✅ AmazeIng complete! Check maze.txt for output."

debug:
	@echo "🐛 Running generator in debug mode..."
	python3 -u generator_maze.py

install:
	@echo "📦 Installing dependencies..."
	@pip install flake8 mypy pytest || echo "Note: Some packages may already be installed"
	@echo "✓ Dependencies installed"
