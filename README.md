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

Explain how the application can be deployed to a production environment. Describe any additional steps or configurations required for deployment, such as setting up a web server or database server.

## Contributing

Provide guidelines for other developers who want to contribute to the project. Include information on how to set up a development environment, coding conventions, and the process for submitting pull requests.

## License

Specify the license under which the project is distributed. For example, you can use the MIT License or any other open-source license that suits your needs.

## Acknowledgements

If you used any external libraries, frameworks, or resources in your project, acknowledge them here and provide links to their documentation or websites.

## Contact

Provide contact information for the project maintainer or team, such as email addresses or links to social media profiles.

