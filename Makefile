.PHONY: lint scraper
lint:
	npx -y @redocly/cli lint api/openapi.yaml

scraper:
	python3 docs_scraper.py

.PHONY: help
help:
	@echo "Available targets:"
	@echo "  lint     - Validate OpenAPI specification using Redocly"
	@echo "  scraper  - Run the documentation scraper"
	@echo "  help     - Show this help message"