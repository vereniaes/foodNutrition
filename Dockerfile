# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY ./requirements.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt
# Use --no-cache-dir to reduce image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code into the container at /app
COPY . /app

# The command to run the application
# Use 0.0.0.0 to make it accessible from outside the container
# The app will run on port 80 inside the container
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]