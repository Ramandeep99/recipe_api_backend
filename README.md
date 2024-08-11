# Recipe API Service

This project is a Django-based API service for managing recipes, user authentication, and user profiles. It includes features like user registration, login, bookmarking recipes, and updating user profiles. The service also integrates Celery for handling asynchronous tasks.

## Setup Commands

```bash
# Clone the Repository

# Create and Activate Virtual Environment
python3 -m venv venv
source venv/bin/activate

# Install Requirements
pip install -r requirements.txt

# Apply Migrations
python manage.py migrate

# Create a Superuser (Optional, for Admin Access)
python manage.py createsuperuser

# Start the Django Development Server
python manage.py runserver

# Start Redis Server (in a separate terminal if necessary)
redis-server

# Start Celery Worker
celery -A recipe worker --loglevel=info

# Start Celery Beat (for periodic tasks)
celery -A recipe beat --loglevel=info

# Run Test Cases
pytest

# Install Coverage Tool
pip install coverage

# Run Tests with Coverage
coverage run --source='.' manage.py test

# Generate Coverage Report
coverage report

# Generate HTML Coverage Report
coverage html


## Docker Setup Commands

# Run a One-off Command: It will run a one-off command in a new container based on the web service defined in your docker-compose.yml file.
docker compose run web django-admin startproject recipe_api /app/new_project

# Build Docker Image
docker-compose build

# Run the Application with Docker
docker-compose up

# Run Migrations with Docker
docker-compose run web python manage.py migrate

# Create Superuser with Docker (if needed)
docker-compose run web python manage.py createsuperuser

# Start the entire setup with Celery Workers using Docker
docker-compose up -d

# View logs of Celery workers
docker-compose logs -f worker

