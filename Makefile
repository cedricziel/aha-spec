.PHONY: lint scraper readme stats build-docs bump-version
lint:
	npx -y @redocly/cli lint api/openapi.yaml

scraper:
	python3 docs_scraper.py

readme:
	python3 generate_readme.py

stats:
	npx -y @redocly/cli stats api/openapi.yaml

build-docs:
	npx -y @redocly/cli build-docs api/openapi.yaml --output ./docs/index.html

bump-version:
	python3 bump_version.py patch

.PHONY: help
help:
	@echo "Available targets:"
	@echo "  lint       - Validate OpenAPI specification using Redocly"
	@echo "  scraper    - Run the documentation scraper"
	@echo "  readme     - Generate README.md from OpenAPI specification"
	@echo "  stats      - Show API statistics using Redocly"
	@echo "  build-docs - Build HTML documentation using Redocly"
	@echo "  bump-version - Bump the API version (patch level)"
	@echo "  help       - Show this help message"