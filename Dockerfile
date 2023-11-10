# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . /usr/src/app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir streamlit pandas pillow

# Make port 8501 available to the world outside this container
EXPOSE 8502

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["streamlit", "run", "app_scoring.py"]
