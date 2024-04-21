# Base image
FROM python:3.8-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy rest of the application
COPY . .

# Expose the port the app runs on
EXPOSE 1000

# Command to run the application
CMD ["python", "api_server.py"]
