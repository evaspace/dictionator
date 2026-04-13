# --- Dicto Maker Makefile ---
# Custom Dictionary Generator Automation

.PHONY: help install run clean

# Default target: display help
help:
	@echo "Dicto Maker - Management Commands"
	@echo "================================="
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@echo "  install   Install required dependencies (pip)"
	@echo "  run       Execute the generator in interactive mode"
	@echo "  clean     Remove temporary Python cache files"
	@echo "  help      Display this information"
	@echo ""
	@echo "Example to save to file:"
	@echo "  python3 dicto_makers/main.py > my_dict.txt"

# Install dependencies from requirements.txt
install:
	@echo "[*] Installing dependencies (forcing system package installation)..."
	pip install -r requirements.txt --break-system-packages

# Run the tool
run:
	@echo "[*] Starting Dicto Maker..."
	python3 main.py

# Cleanup __pycache__ and temp files
clean:
	@echo "[*] Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "[+] Cleanup complete."
