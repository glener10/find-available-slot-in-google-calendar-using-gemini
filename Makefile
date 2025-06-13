SHELL := /bin/bash

.PHONY: run clean

run:
	@echo "Checking for 'venv' virtual environment..."
	@if [ ! -d "venv" ]; then \
    echo "'venv' virtual environment not found. Creating and installing dependencies..."; \
    python3 -m venv venv; \
    source venv/bin/activate && venv/bin/pip3 install -r requirements.txt; \
    echo "Installation complete!"; \
	fi
	@echo "Activating virtual environment and running the application..."
	source venv/bin/activate && venv/bin/python3 main.py

clean:
	@echo "Removing virtual environment and temporary files..."
	rm -rf venv
	find . -name "__pycache__" -exec rm -rf {} +
	find . -name "*.pyc" -exec rm -f {} +