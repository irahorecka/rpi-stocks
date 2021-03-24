black: ## black format every python file to line length 100
	find . -type f -name "*.py" | xargs black --line-length=100;
	find . -type d -name "__pycache__" | xargs rm -r;