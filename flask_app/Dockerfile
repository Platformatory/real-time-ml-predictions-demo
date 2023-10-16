# Use the official Python image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the application code and model into the container
COPY . .

# Install the required dependencies
RUN pip install -r requirements.txt

# Expose the port your Flask app will run on
EXPOSE 5000

# Start the Flask app
CMD ["python", "predict.py"]