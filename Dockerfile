# Use Ubuntu as the base image
FROM ubuntu:20.04

# Update and upgrade the base image
RUN apt-get update && apt-get upgrade -y

# Install Java
RUN apt-get install -y openjdk-11-jre

# Install Python and pip
RUN apt-get install -y python3 python3-pip

# Clean up the package manager cache to reduce the image size
RUN apt-get clean

# Set the default Python version to 3
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1

# Verify the installed versions
RUN java -version
RUN python --version

# Set the default working directory
WORKDIR /app

# Copy the required files
COPY feature_repo/ feature_repo

RUN sed -i 's/localhost:6379/redis:6379/g' feature_repo/feature_store.yaml
RUN sed -i 's/localhost:5432/postgres:5432/g' feature_repo/feature_store.yaml
RUN sed -i 's/localhost:9092/kafka:9071/g' feature_repo/data_sources.py

COPY get_predictions.py get_predictions.py

RUN sed -i 's/localhost:5001/modelapi:5001/g' get_predictions.py

COPY ingest_stream.py ingest_stream.py
COPY requirements.txt requirements.txt

# Install the python dependencies
RUN pip install -r requirements.txt
