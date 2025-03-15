gcloud compute instance-templates create my-template \
    --machine-type=e2-medium \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud \
    --metadata=startup-script='#!/bin/bash
      sudo apt update
      sudo apt install -y nginx
      sudo systemctl start nginx'

