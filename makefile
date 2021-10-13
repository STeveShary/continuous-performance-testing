.PHONY: build
build: ## Build the docker image.
	docker build -t continuous-test-server -f server.test.dockerfile .
	docker build -t locust-ui -f locust.ui.dockerfile .
	docker build -t locust-test -f locust.test.dockerfile .

.PHONY: run-server
run-server: build ## Run the server locally for interactive performance testing
	docker run -it -p 5000:5000 continuous-test-server

.PHONY: run-server-daemon
run-server-daemon: build ## Run the server locally for interactive performance testing
	docker run -d -p 5000:5000 continuous-test-server

.PHONY: run-locust
run-locust: build ## Run the server locally for interactive performance testing
	docker-compose down
	docker-compose up -f locust.ui.dockerfile

.PHONY: test-locust
test-locust: build ## Run the server locally for interactive performance testing
	docker-compose -f docker-compose.test.yaml up
