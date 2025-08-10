# Start with an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# ---- COMPREHENSIVE DEPENDENCIES FOR WEASYPRINT ----
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libffi-dev \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    libpangoft2-1.0-0 \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*
# ----------------------------------------------------

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire resume-optimizer directory into the container
COPY ./resume-optimizer /app/resume-optimizer

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Define the command to run your app when the container starts
CMD ["streamlit", "run", "resume-optimizer/app.py", "--server.port=8501", "--server.address=0.0.0.0"]