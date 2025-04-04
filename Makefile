.PHONY: help setup-poly-keys test test-unit test-integration run-api

help:
	@echo "Available commands:"
	@echo "  setup-poly-keys     Generate Polymarket API keys (requires --private-key)"
	@echo "  test               Run all tests (excluding integration tests)"
	@echo "  test-unit          Run unit tests only"
	@echo "  test-integration   Run integration tests only"
	@echo "  run-api            Run the API server"
	@echo ""
	@echo "Example:"
	@echo "  make setup-poly-keys private_key=0x123... [proxy=0x456...] [type=0] [env_file=.env]"

setup-poly-keys:
	@if [ -z "$(private_key)" ]; then \
		echo "Error: --private-key is required"; \
		echo "Usage: make setup-poly-keys private_key=0x... [proxy=0x...] [type=0] [env_file=.env]"; \
		exit 1; \
	fi
	@echo "Generating Polymarket API keys..."
	@python -m services.auth.setup_api_key \
		--private-key $(private_key) \
		$(if $(proxy),--proxy $(proxy)) \
		$(if $(type),--type $(type)) \
		$(if $(env_file),--env-file $(env_file))

test:
	pytest -v -m "not integration"

test-unit:
	pytest -v -m "not integration"

test-integration:
	RUN_INTEGRATION_TESTS=1 pytest -v -m integration

run-api:
	@echo "Starting API server..."
	@cd api && python run.py 