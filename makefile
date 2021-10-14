.PHONY: build
build: ## Build the docker images.
	docker build -t continuous-test-server -f server.test.dockerfile .
	docker build -t locust-ui -f locust.ui.dockerfile .
	docker build -t locust-test -f locust.test.dockerfile .

.PHONY: run-locust
run-locust: build ## Run the server locally for interactive performance testing
	docker-compose -f docker-compose.ui.yaml up

.PHONY: test-locust
test-locust: build ## Run the server locally for interactive performance testing
	docker-compose -f docker-compose.test.yaml up
