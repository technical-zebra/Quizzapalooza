FROM python:3.11.4-slim-bullseye

LABEL Name="Django App" Version=1.0.0
LABEL org.opencontainers.image.source="https://github.com/technical-zebra/Quizzapalooza"

# Set the working directory
WORKDIR /app

# Copy the Django project files
COPY src/requirements.txt .
COPY src/manage.py .
COPY src/Quizzapalooza/ ./Quizzapalooza/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Collect static files (if needed)
# RUN python manage.py collectstatic --noinput

# Expose the application's port
EXPOSE 8000

# Specify the command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]