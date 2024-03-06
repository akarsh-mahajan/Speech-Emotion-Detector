# Use the official Python image with version 3.9 as the base
FROM python:3.9

# Create a working directory and copy the project directory into it
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the rest of the project files into the working directory
COPY . .

# Expose the port that Django typically uses (8000)
EXPOSE 8000

# Set the command to be executed when the container starts
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
