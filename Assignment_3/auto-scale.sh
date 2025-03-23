#!/bin/bash
CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print $2 + $4}')
THRESHOLD=75.0

if (( $(echo "$CPU_USAGE > $THRESHOLD" | bc -l) )); then
    echo "High CPU usage detected: $CPU_USAGE%"
    gcloud compute instances create scaled-vm --machine-type=e2-standard-2 --image-family=ubuntu-2004-lts --image-project=ubuntu-os-cloud
fi
