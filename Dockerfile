# Use an official Python runtime as a parent image
FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and set the working directory
WORKDIR /SocialNetAPI

# Copy the current directory contents into the container at /tanxfi_task
COPY . /SocialNetAPI

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Apply database migrations
RUN python manage.py makemigrations
RUN python manage.py migrate

# Expose port 8000
EXPOSE 8000

# Start the application using multiple CMD commands
CMD python manage.py runserver 0.0.0.0:8000 