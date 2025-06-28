SHELL := $(shell echo $$SHELL)

.PHONY: run clean

run:
	@# Este bloco inteiro é executado em um único shell por causa das barras invertidas
	@echo "Checking for 'venv' virtual environment..."
	@if [ ! -d "venv" ]; then \
		echo "'venv' virtual environment not found. Creating and installing dependencies..."; \
		python3 -m venv venv; \
		source venv/bin/activate && pip3 install -r requirements.txt; \
		echo "Installation complete!"; \
	fi; \
	echo "Activating virtual environment and running the application..."; \
	source venv/bin/activate && python3 main.py $(ARGS)

clean:
	@echo "Removing virtual environment and temporary files..."
	rm -rf venv
	find . -name "__pycache__" -exec rm -rf {} +
	find . -name "*.pyc" -exec rm -f {} +