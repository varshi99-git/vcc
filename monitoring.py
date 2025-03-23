# Auto-scaling script using Prometheus and GCP
import requests
import time
from google.cloud import compute_v1

# Configuration
PROMETHEUS_URL = "http://localhost:9090/api/v1/query"
CPU_QUERY = "100 - (avg by (instance) (irate(node_cpu_seconds_total{mode='idle'}[5m])) * 100)"
THRESHOLD = 75.0
GCP_PROJECT = "your-gcp-project-id"
GCP_ZONE = "us-central1-a"
INSTANCE_TEMPLATE = "your-instance-template"
INSTANCE_GROUP = "your-instance-group"

# Function to fetch CPU utilization
def get_cpu_usage():
    response = requests.get(PROMETHEUS_URL, params={"query": CPU_QUERY})
    result = response.json()
    if result["status"] == "success":
        values = result["data"]["result"]
        if values:
            return float(values[0]["value"][1])
    return 0.0

# Function to scale up GCP instances
def scale_up():
    client = compute_v1.InstanceGroupManagersClient()
    instance_group_manager = client.get(project=GCP_PROJECT, zone=GCP_ZONE, instance_group_manager=INSTANCE_GROUP)
    current_size = instance_group_manager.target_size
    new_size = current_size + 1
    print(f"Scaling up: Increasing instances from {current_size} to {new_size}")
    client.resize(project=GCP_PROJECT, zone=GCP_ZONE, instance_group_manager=INSTANCE_GROUP, size=new_size)

# Monitoring loop
while True:
    cpu_usage = get_cpu_usage()
    print(f"Current CPU Usage: {cpu_usage}%")
    if cpu_usage > THRESHOLD:
        scale_up()
    time.sleep(60)
