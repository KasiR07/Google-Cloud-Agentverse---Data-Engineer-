#!/bin/bash

# This script sets up the necessary Google Cloud Storage buckets and uploads
# initial data files. It is designed to be run AFTER sourcing the
# set_env.sh script, as it depends on variables like PROJECT_ID and BUCKET_NAME.

# --- Pre-flight Check ---
# Ensure that the required environment variables have been set.
if [ -z "$PROJECT_ID" ] || [ -z "$BUCKET_NAME" ] || [ -z "$REGION" ]; then
  echo "Error: Required environment variables (PROJECT_ID, BUCKET_NAME, REGION) are not set."
  echo "Please run 'source ./set_env.sh' before executing this script."
  exit 1
fi

echo "--- Starting GCS Data Setup for Project: $PROJECT_ID ---"

# --- 1. Create GCS Buckets ---
# This script uses one buckets:
#   - gs://<project-id>-reports (for processed data, scrolls, etc.) -> $BUCKET_NAME

echo "Checking/creating bucket: gs://$BUCKET_NAME"
# Create the bucket only if it doesn't already exist.
gcloud storage buckets describe gs://$BUCKET_NAME >/dev/null 2>&1 || \
  gcloud storage buckets create gs://$BUCKET_NAME --project=$PROJECT_ID --location=$REGION --uniform-bucket-level-access

# --- 2. Upload Raw Report Files ---
# These files represent the initial raw data to be processed.
REPORTS_DIR=~/agentverse-dataengineer/data/reports
if [ -d "$REPORTS_DIR" ]; then
  echo "Uploading report files from $REPORTS_DIR..."
  cd $REPORTS_DIR
  # The destination is the bucket named after the project ID, in a 'raw_intel' folder.
  gcloud storage cp report_*.txt gs://${BUCKET_NAME}/raw_intel/ --quiet
else
  echo "Warning: Directory not found, skipping report upload: $REPORTS_DIR"
fi


# --- 3. Upload Ancient Scroll Files ---
# These files represent knowledge base or context documents.
SCROLLS_DIR=~/agentverse-dataengineer/data/scrolls_chest
if [ -d "$SCROLLS_DIR" ]; then
  echo "Uploading scroll files from $SCROLLS_DIR..."
  cd $SCROLLS_DIR
  # The destination is the primary bucket for the project, in an 'ancient_scrolls' folder.
  gcloud storage cp scroll_*.md gs://${BUCKET_NAME}/ancient_scrolls/ --quiet
else
  echo "Warning: Directory not found, skipping scroll upload: $SCROLLS_DIR"
fi

# Return to the original directory
cd - > /dev/null

echo ""
echo "--- Data setup complete ---"