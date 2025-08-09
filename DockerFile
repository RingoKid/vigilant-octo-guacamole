# Start with an official Python runtime as a parent image
# This is more lightweight than the devcontainer image for production
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# This bakes the dependencies directly into the image
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire resume-optimizer directory into the container
COPY ./resume-optimizer /app/resume-optimizer

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Define the command to run your app when the container starts
CMD ["streamlit", "run", "resume-optimizer/app.py", "--server.port=8501", "--server.address=0.0.0.0"]