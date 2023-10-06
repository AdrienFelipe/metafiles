# -STAGE: Base
FROM python:3.9-slim AS base

SHELL ["/bin/bash", "-c"]

# Update pip
RUN pip install --upgrade pip --no-cache-dir

# Install prod requirements.
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt && rm -f /tmp/requirements.txt


# -STAGE: Production
FROM base AS prod

COPY src/ /app

WORKDIR /app


# -STAGE: Development
FROM base AS dev

# Install development-only dependencies
RUN apt-get update
RUN apt-get install -y git

# Install dev requirements.
COPY requirements-dev.txt /tmp/
RUN pip install -r /tmp/requirements-dev.txt && rm -f /tmp/requirements-dev.txt

WORKDIR /workspace

# Keep container up.
CMD ["tail", "-f", "/dev/null"]
