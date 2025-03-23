# Cloud Auto-Scaling Setup

## Overview
This project provides an automated method to monitor CPU usage on a local VM and scale resources to the cloud (GCP) when usage exceeds a defined threshold.

## Features
- Monitors CPU usage using Prometheus.
- Automatically scales up instances in Google Cloud when CPU exceeds 75%.
- Uses Google Cloud Instance Groups for auto-scaling.

## Prerequisites
- Google Cloud SDK installed and authenticated.
- Prometheus set up for monitoring.
- Python 3 installed with `requests` and `google-cloud-compute` modules.

## Usage
1. Update configuration variables in `monitoring.py`.
2. Run `python monitoring.py` to start monitoring and auto-scaling.

## License
MIT License
