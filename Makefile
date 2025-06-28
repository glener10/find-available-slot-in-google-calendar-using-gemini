SHELL := $(shell echo $$SHELL)
VENV_DIR = .venv
VENV_PYTHON = $(VENV_DIR)/bin/python
VENV_RUFF = $(VENV_DIR)/bin/ruff

.PHONY: setup lint format test run clean

setup:
	@echo "Checking for '$(VENV_DIR)' virtual environment..."
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "'$(VENV_DIR)' not found. Creating and installing dependencies..."; \
		python3 -m venv $(VENV_DIR); \
		$(VENV_PYTHON) -m pip install --upgrade pip; \
		$(VENV_PYTHON) -m pip install -r requirements.txt; \
		echo "Setup complete!"; \
	else \
		echo "'$(VENV_DIR)' already exists. To reinstall, run 'make clean setup'."; \
	fi

lint: setup
	@echo "Linting code with ruff..."
	@$(VENV_RUFF) check .

format: setup
	@echo "Formatting code with ruff..."
	@$(VENV_RUFF) format .

test: setup
	@echo "Running tests..."
	@$(VENV_PYTHON) -m unittest discover -v

run: setup
	@echo "Running the application..."
	@$(VENV_PYTHON) main.py $(ARGS)

clean:
	@echo "Removing virtual environment and temporary files..."
	@rm -rf $(VENV_DIR)
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete