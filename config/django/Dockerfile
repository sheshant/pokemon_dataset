# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Copy requirements.txt to the working directory
COPY requirements.txt /app/

# Install any necessary dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Run migrations and collect static files (for production setup)
RUN python manage.py migrate
RUN python manage.py collectstatic --no-input

# Expose the port the app runs on
EXPOSE 8000

# Command to run Gunicorn server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "pokemon_dataset.wsgi:application", "--workers", "3"]
