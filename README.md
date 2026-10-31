# Yuno Payment Infrastructure – DevOps Assignment

## Overview
A containerized payment transaction processing application with monitoring and observability.

## Technology Stack
- Ubuntu / WSL2
- Python 3.12
- Docker
- Docker Compose
- Prometheus
- Grafana
- GitHub Actions

## Architecture
Payment Client -> Payment API -> Prometheus -> Grafana

## Application
The API provides:
- Payment authorization endpoint
- Health check endpoint
- Application metrics

## Docker
Build:
docker build -t yuno-txn-processor:v1 .

Run:
docker compose up -d

Stop:
docker compose down

## Monitoring
Prometheus collects application metrics.
Grafana visualizes:
- Total payment requests
- Request rate
- API error rate
- p95 latency
- SLO compliance

## CI/CD
GitHub Actions automatically:
- Checks out source code
- Installs Python dependencies
- Validates Python syntax
- Builds Docker image
- Validates Docker Compose configuration

## Security
Sensitive configuration files are excluded using .gitignore.
