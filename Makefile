.PHONY: format lint

format:
	${INFO} "Formatting code..."
	isort src tests
	black src tests
	${INFO} "Code formated"

lint:
	${INFO} "Linting code..."
	flake8 src tests
	${INFO} "Code linted"

# Cosmetics
YELLOW := "\e[1;33m"
NC := "\e[0m"

#Shell Functions
INFO := @bash -c '\
	printf $(YELLOW); \
	echo "=> $$1"; \
	printf $(NC)' VALUE