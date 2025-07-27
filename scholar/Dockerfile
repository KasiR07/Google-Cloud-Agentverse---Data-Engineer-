# Use an official, lean Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container for all subsequent commands
WORKDIR /app

# Upgrade pip to ensure we have the latest features and security patches
RUN pip install --upgrade pip

# --- Dependency Installation ---
# Copy only the requirements file first to leverage Docker's build cache.
# This step is only re-run if requirements.txt changes.
COPY ./scholar/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# --- Application Code ---
# Copy the entire scholar application code into the container
COPY ./scholar /app/scholar

# --- Environment ---
# Add the application directory to the PYTHONPATH so modules can be found.
ENV PYTHONPATH=/app

# --- Expose Port ---
# Make port 8080 available to the world outside this container.
# Google Cloud Run uses the PORT environment variable to send traffic to your app.
EXPOSE 8080

# --- Run the Application ---
# Define the command to run when the container launches.
# Using '-m' runs the module as a script, which works perfectly with our PYTHONPATH setup.
CMD ["python", "-m", "scholar.a2a_server"]
