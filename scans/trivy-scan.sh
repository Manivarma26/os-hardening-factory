#!/usr/bin/env bash
set -e

IMAGE_ID=$1
REGION="ap-south-1"
OUTPUT="outputs/reports/trivy-report-${IMAGE_ID}.json"

echo "🔍 Running Trivy vulnerability scan on AMI: $IMAGE_ID"

# Pull AMI info and run scan (requires trivy + AWS CLI)
trivy aws --region $REGION --security-checks vuln --format json --output $OUTPUT aws-account-id $IMAGE_ID

echo "✅ Trivy scan complete: $OUTPUT"
