# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install Vim and any other dependencies
# RUN apt-get update
# && apt-get install -y vim && apt-get clean

# Copy the current directory contents into the container at /app
COPY . /app

# Set up the Datadog log collection configuration
LABEL "com.datadoghq.ad.logs"='[{"type":"file", "path":"/app/prime_number.log", "service":"prime_number_app", "source":"python"}]'


# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8083 available to the world outside this container
EXPOSE 8083

# Define environment variables for Datadog (Optional if you use environment variables)
ENV DD_AGENT_HOST=host.docker.internal
# ENV DD_API_KEY=DD_API_KEY
# echo "YOUR_API_KEY" | docker secret create dd_api_key -
# echo "YOUR_APP_KEY" | docker secret create dd_app_key -
ENV DD_APP_KEY= 
ENV DD_API_KEY= 

# Run prime_number.py when the container launches
CMD ["python", "prime_number.py"]
