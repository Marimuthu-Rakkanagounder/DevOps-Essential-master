# Use the official Python image as a base image
FROM python:3.8-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Expose the port the app runs on
EXPOSE 5000

# Install Gunicorn
RUN pip install gunicorn

# Run Gunicorn to serve the Flask app
CMD ["gunicorn", "--config", "gunicorn_config.py", "app:app"]
