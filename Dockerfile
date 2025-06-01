# Use an official lightweight Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the dependency list into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install -r requirements.txt

# Copy the rest of your application code into the container
COPY . .

# Tell Docker what command to run when the container starts
CMD ["python", "app.py"]