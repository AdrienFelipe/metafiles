SERVICE_NAME=app
DOCKER_COMPOSE=docker-compose


# Bring down the Docker container and remove orphan containers
rm:
	$(DOCKER_COMPOSE) down --remove-orphans

# Bring up the Docker container
up:
	$(DOCKER_COMPOSE) up -d

# Build the Docker image
build:
	$(DOCKER_COMPOSE) build $(SERVICE_NAME)

# Build and run the Docker image
start: rm build up

# Run project tests
test:
	$(DOCKER_COMPOSE) exec $(SERVICE_NAME) python -m unittest discover -s tests


# Run Code Analyzer
ca:
	$(DOCKER_COMPOSE) exec $(SERVICE_NAME) flake8 src tests

# Apply Code Styles
cs:
	$(DOCKER_COMPOSE) exec $(SERVICE_NAME) black src tests

# Run the actual application
run:
	$(DOCKER_COMPOSE) run --service-ports $(SERVICE_NAME) python main.py
