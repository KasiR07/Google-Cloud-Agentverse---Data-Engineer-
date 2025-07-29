# Use an official Dataflow base image for our golem's foundation.
FROM gcr.io/dataflow-templates-base/python312-template-launcher-base

# Set the working directory inside the container.
WORKDIR /dataflow

ENV GOOGLE_GENAI_USE_VERTEXAI=TRUE
ARG GOOGLE_CLOUD_PROJECT
ARG GOOGLE_CLOUD_LOCATION
ENV GOOGLE_CLOUD_PROJECT=${GOOGLE_CLOUD_PROJECT}
ENV GOOGLE_CLOUD_LOCATION=${GOOGLE_CLOUD_LOCATION}

# Copy the Scribes' tools (requirements) first. This is a Docker caching optimization.
COPY requirements.txt .

# Inscribe the golem with the necessary tools.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the Scriptorium's incantations.
COPY . .

# This tells Dataflow which master incantation to run when the golem is summoned.
ENV FLEX_TEMPLATE_PYTHON_PY_FILE=batch_inscribe_pipeline.py