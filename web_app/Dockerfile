# Base image
FROM python:3.8-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt


COPY . .

# Expose the port the app runs on
EXPOSE 5001
 
# Command to run the
CMD ["python", "app.py", "--host=0.0.0.0", "--port=5001"]