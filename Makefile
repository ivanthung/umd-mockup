.PHONY: lint format imports clean

lint:
	pylint .

format:
	poetry run black --config pyproject.toml .
	isort .

imports:
	pycln .

clean:
    # Add commands to remove generated files or temporary output if needed
