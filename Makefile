# Makefile

# Variables
PYTHON_CMD := poetry run python

# Help: Display the help section
# Help: Display the help section
help:
	@rem Display the help section
	@set BLANK_LINE= 
	@echo Description:
	@echo   This software extracts the Windows license key if provided.
	@echo	.
	@echo Available targets:
	@echo   help                   Display this help message.
	@echo   install                Install all dependencies.
	@echo   run                    Run the script to extract Windows license key.
	@echo   clean                  Remove Python cache files.
	@echo   check_dependencies     Check poetry dependencies
	@echo Usage:
	@echo   make [target]

# Run: Execute the Python script using Poetry
run:
	@$(PYTHON_CMD) main.py

check_dependencies:
	@echo "Running hard check for dependencies..."
	poetry check
	poetry install --no-root --dry-run

# Init: Install dependencies using Poetry
install:
	poetry lock --no-update
	poetry install --no-root

# Clean: Remove Python cache files (Windows version)
clean:
	@for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
	@for /r . %%f in (*.pyc) do @if exist "%%f" del /q "%%f"