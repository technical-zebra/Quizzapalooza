# Quizzapalooza - A Kahoot-like Web Application

Quizzapalooza is a web application developed using HTML, CSS, JavaScript, and Django. It provides an interactive learning platform where educators can create quizzes and learners can participate in engaging quiz sessions. The application follows the MVT (Model-View-Template) architecture and incorporates user authentication, quiz management, waiting halls, and competition sessions.

## Key Features

- User authentication: Users can create accounts, log in, and log out.
- Quiz creation/deletion: Educators can create and delete quizzes with multiple-choice or true/false questions.
- Waiting hall: Students can join quiz sessions by providing a session ID and nickname.
- Competition session: Quizzes are conducted in a competitive environment with both teachers and students.
- Efficient server-client communication: Django channels and jQuery are used for real-time communication.
- Database integration: PostgreSQL is used for quiz data storage, while MongoDB is used for competition data storage.
- CI/CD pipeline: A GitLab CI/CD pipeline is set up for testing, building Docker images, and deployment to Azure.


## Challenges and different implementation options

During the development of Quizzapalooza, I encountered several challenges that required thoughtful solutions. One of the challenges was implementing real-time communication between the server and clients. To address this, we utilized Django channels, an alternative to Socket.io, to facilitate efficient server-client communication. This allowed for seamless interactions during quiz sessions, such as displaying real-time leaderboard updates and receiving live responses from participants.

Another challenge I faced was storing and managing quiz and competition data. To handle quiz data, I integrated a PostgreSQL database, ensuring efficient storage and retrieval of quizzes created by educators. For competition data, I utilized MongoDB, a NoSQL database, to store information about competition sessions and participants.

## Screenshots
### Login Page
![Login Page](https://github.com/technical-zebra/Coursework_3405/blob/main/Screenshots/Picture1.png "Login Page")


### Sign up Page
![Sign up Page](https://github.com/technical-zebra/Coursework_3405/blob/main/Screenshots/Picture2.png "Sign up Page")


### Create quiz Page (multi-choices)
![Create quiz Page (multi-choices)](https://github.com/technical-zebra/Coursework_3405/blob/main/Screenshots/Picture3.png "Create quiz Page (multi-choices)")


### Create quiz Page (true or false)
![Create quiz Page (true or false)](https://github.com/technical-zebra/Coursework_3405/blob/main/Screenshots/Picture4.png "Create quiz Page (true or false)")


### Display quiz Page
![Display quiz Page](https://github.com/technical-zebra/Coursework_3405/blob/main/Screenshots/Picture5.png "Display quiz Page")


### Waiting hall (Teacher)
![Create quiz Page (true or false)](https://github.com/technical-zebra/Coursework_3405/blob/main/Screenshots/Picture6.png "Create quiz Page (true or false)")


### Waiting hall (Student)
![Waiting hall (Student)](https://github.com/technical-zebra/Coursework_3405/blob/main/Screenshots/Picture7.png "Waiting hall (Student)")


### Join quiz Page (Student)
![Join quiz Page (Student)](https://github.com/technical-zebra/Coursework_3405/blob/main/Screenshots/Picture8.png "Join quiz Page (Student)")


### Run Quiz(Student)
![Run Quiz(Student)](https://github.com/technical-zebra/Coursework_3405/blob/main/Screenshots/Picture8.png "Run Quiz(Student)")


### Run Quiz(Teacher)
![Run Quiz(Teacher)](https://github.com/technical-zebra/Coursework_3405/blob/main/Screenshots/Picture10.png "Run Quiz(Teacher)")


### Winner Page
![Winner Page](https://github.com/technical-zebra/Coursework_3405/blob/main/Screenshots/Picture11.png "Winner Page")

## Getting Started

Provide instructions on how to set up and run the application locally. Include any necessary prerequisites, such as Python and Django versions, and provide step-by-step instructions to install dependencies and run the application.

## Getting Started

To set up and run the application locally, follow these steps:

### Prerequisites

Make sure you have the following prerequisites installed on your system:

- Python (version 3.11)
- Pipenv (version 2023.5.19)

### Installation

1. Clone the repository to your local machine:

   ```
   git clone <repository_url>
   ```

2. Navigate to the project directory:

   ```
   cd quizzapalooza_app
   ```

3. Create a virtual environment and install dependencies using Pipenv:

   ```
   pipenv install
   ```
   ```
   pipenv shell
   ```
    ```
   pipenv install --dev
   ```
   

4. Navigate to the project directory:

   ```
   cd quizzapalooza_app
   ```
### Setting up databse

To set up the Django database for the first time, you need to follow these steps:

1. Configure the Database Settings:
   Open your Django project's settings file (`settings.py`) and locate the `DATABASES` configuration. Modify the following settings according to your database setup:
   
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.<database_engine>',
           'NAME': '<database_name>',
           'USER': '<database_user>',
           'PASSWORD': '<database_password>',
           'HOST': '<database_host>',
           'PORT': '<database_port>',
       }
   }
   ```
   
   Replace `<database_engine>` with the engine you're using (e.g., `postgresql`, `mysql`, `sqlite3`, etc.), and provide the appropriate values for `<database_name>`, `<database_user>`, `<database_password>`, `<database_host>`, and `<database_port>`.
   
   If you're using SQLite as your database engine, you can skip the rest of the steps as SQLite doesn't require additional setup.

2. Create the Database (for non-SQLite databases):
   If you're using a non-SQLite database engine, you need to create an empty database before running Django's migrations. The process for creating a database depends on the specific database system you're using. Refer to your database's documentation for instructions on creating a new database.

3. Apply Migrations:
   Once the database settings are configured, you can apply Django's migrations to set up the necessary database tables and schema. Run the following command in your project's root directory (where the `manage.py` file is located):
   
   ```shell
   python manage.py migrate
   ```
   
   This command will create the required tables in the database based on your Django project's models.

4. Create a Superuser (optional):
   If you want to create a superuser account to access the Django admin site, you can use the following command:
   
   ```shell
   python manage.py createsuperuser
   ```
   
   Follow the prompts to provide a username, email (optional), and password for the superuser account.

Once you have completed these steps, your Django database should be set up and ready to use.
### Running the Application

Once the installation is complete, you can run the application using the following command:

```
pipenv run python manage.py runserver
```

This will start the Django development server, and you can access the application by visiting `http://localhost:8000` in your web browser.

### Running Tests

To run the tests for the application, use the following command:

```
pipenv run python manage.py test
```

This will execute the test suite and display the test results in the console.



## Deployment

This repository contains the implementation of the CI/CD pipeline for the Quizzapalooza application using Docker Hub. The pipeline ensures efficient version tracking, collaboration, testing, and deployment of the application.

### Pipeline Overview

1. Version Control:
   - The Quizzapalooza source code is hosted on GitLab, a version control system.
   - Developers commit code changes to the Git repository, enabling version tracking and collaboration.

2. Triggering the Pipeline:
   - The CI/CD pipeline is automatically triggered when changes are pushed to the Git repository.
   - This ensures that the latest changes are tested and deployed.

3. Testing:
   - The pipeline includes a testing stage where automated tests are executed to validate the functionality and quality of the application.
   - Various types of tests, such as unit tests, integration tests, and other relevant tests, are performed to ensure the application meets the desired criteria.

4. Building a Docker Image:
   - After passing the tests, the pipeline builds a Docker image of the application.
   - The Docker image encapsulates the application and its dependencies, ensuring consistency and portability across different environments.

5. Pushing the Docker Image to Docker Hub:
   - The Docker image is pushed to Docker Hub, which serves as the container registry.
   - Docker Hub provides a centralized location for storing and managing Docker images.

6. Deployment to Azure:
   - In the deployment stage, the Docker image stored in Docker Hub is pulled to the production environment.
   - The image is then used to spin up containers running the Quizzapalooza application.
   - The deployment is specifically targeted for Azure, a cloud computing platform.

### Deploying to Azure

To deploy the Quizzapalooza application to Azure, the following steps were performed:

1. Azure Account Setup:
   - Set up an Azure account to access the Azure cloud computing platform.

2. Azure Resource Creation:
   - Create the necessary Azure resources, such as a virtual machine or an Azure App Service, to host the Quizzapalooza application.

3. Containerization with Docker:
   - Build a Docker image of the Quizzapalooza application as part of the CI/CD pipeline.
   - Ensure that the Docker image contains all the necessary dependencies and configurations.

4. Azure Container Registry:
   - Set up an Azure Container Registry to store the Docker image.
   - This registry acts as a private repository for the application's container images.

5. Deploying with Azure Container Instances or Azure Kubernetes Service:
   - Choose the appropriate Azure service, such as Azure Container Instances or Azure Kubernetes Service (AKS), for deploying the Quizzapalooza application.
   - Configure the chosen service to pull the Docker image from the Azure Container Registry and run the application containers.


## Acknowledgements

The following external libraries and frameworks were used in the Quizzapalooza project:

Django: A high-level Python web framework used for rapid development, providing a clean and efficient design for building web applications.

Django Channels: A library that extends Django's capabilities to handle real-time communication and WebSocket protocols, enabling efficient server-client communication during quiz sessions.

djongo: A MongoDB connector for Django that allows seamless integration with MongoDB, facilitating the storage and retrieval of competition data in a NoSQL database.

pymongo: A Python driver for MongoDB, providing an interface to interact with the MongoDB database and perform operations like data insertion, retrieval, and querying.

psycopg2: A PostgreSQL adapter for Python that enables Django to connect and interact with a PostgreSQL database, ensuring efficient storage and retrieval of quiz-related information.

channels: A Django library that enables the implementation of asynchronous and event-driven functionalities, allowing real-time updates and communication between the server and clients.

daphne: An HTTP and WebSocket protocol server for Django, used in conjunction with Django Channels to handle and process WebSocket connections.

pytz: A Python library that provides timezone definitions and utilities, ensuring accurate timezone conversions and handling in the application.

six: A compatibility library that provides Python 2 and 3 compatibility utilities, facilitating code compatibility and smooth transitions between Python versions.


