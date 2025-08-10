

gcloud storage buckets create gs://atomic-legacy-467221-f7-reports --project=atomic-legacy-467221-f7 --location=us-central1



cd ~/agentverse-dataengineer/data/reports
gcloud storage cp report_*.txt gs://atomic-legacy-467221-f7/raw_intel/

gcloud storage ls gs://atomic-legacy-467221-f7-reports/raw_intel/

bq mk --connection \
  --connection_type=CLOUD_RESOURCE \
  --project_id=atomic-legacy-467221-f7 \
  --location=us-central1 \
  gcs-connection


  CREATE OR REPLACE MODEL bestiary_data.gemini_pro_model
  REMOTE WITH CONNECTION `atomic-legacy-467221-f7.us-central1.gcs-connection`
  OPTIONS (endpoint = 'gemini-2.5-flash');


cd ~/agentverse-dataengineer/data/scrolls_chest
gcloud storage cp scroll_*.md gs://atomic-legacy-467221-f7-reports/ancient_scrolls/



python inscribe_essence_pipeline.py \
  --runner=DirectRunner \
  --project=$PROJECT_ID \
  --region=$REGION \
  --job_name="grimoire-local-test-$(date +%Y%m%d-%H%M%S)" \
  --temp_location="gs://${BUCKET_NAME}/dataflow/temp" \
  --staging_location="gs://${BUCKET_NAME}/dataflow/staging" \
  --input_pattern="gs://${BUCKET_NAME}/ancient_scrolls/*.txt" \
  --instance_name=$SQL_INSTANCE_NAME






Run local test

```bash
export PROJECT_ID="atomic-legacy-467221-f7"
export REGION="us-central1"
export BUCKET_NAME="atomic-legacy-467221-f7-reports"
export SQL_INSTANCE_NAME="grimoire-spellbook"

# --- The Local Divination Incantation ---
echo "Casting a local divination using the DirectRunner..."

python3 inscribe_essence_pipeline.py \
  --runner=DirectRunner \
  --project=$PROJECT_ID \
  --region=$REGION \
  --job_name="grimoire-local-test-$(date +%Y%m%d-%H%M%S)" \
  --temp_location="gs://${BUCKET_NAME}/dataflow/temp" \
  --staging_location="gs://${BUCKET_NAME}/dataflow/staging" \
  --input_pattern="gs://${BUCKET_NAME}/ancient_scrolls/*.md" \
  --instance_name=$SQL_INSTANCE_NAME
```