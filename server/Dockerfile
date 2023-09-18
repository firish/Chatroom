# Use an official Python runtime as the parent image
FROM python:3.8-slim

# Set the working directory in the Docker container
WORKDIR /app

# Copy the current directory (Flask app) contents into the container at /app
COPY . /app/

# If you have a requirements.txt, use it to install the Python dependencies.
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 5000 available to the world outside this container (Flask's default port)
EXPOSE 5000

# Define environment variable for Flask to run in production mode (remove if you want development mode)
# ENV FLASK_ENV=production

# Run the Flask app
CMD ["python", "app.py"]
