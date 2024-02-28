.PHONY: lint format imports clean
PYTHON_FILES := $(shell find . -name '*.py' -print0 | xargs -0)

lint:
	pylint .

format:
	poetry run black --config pyproject.toml .
	isort .

imports:
	pycln "$(PYTHON_FILES)"

clean:
    # Add commands to remove generated files or temporary output if needed
