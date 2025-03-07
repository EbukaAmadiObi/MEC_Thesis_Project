# Specify base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the necessary files into the container
COPY requirements.txt requirements.txt
COPY KNN.py KNN.py

# Install the required Python libraries
RUN pip install -r requirements.txt

# Run the Python script when the container starts
CMD ["python", "KNN.py"]