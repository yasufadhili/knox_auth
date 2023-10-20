# Project Documentation: Knox Auth

## Overview - The users App

The "Users" app is a Django application designed for user management and user-related features. It includes functionalities such as user registration, user profiles, user relationships (followers and following), and user authentication using [Django Rest Knox](https://jazzband.github.io/django-rest-knox/). This documentation provides a detailed guide on how to use the "Users" app and its API endpoints.

## Table of Contents

- [Installation](#installation)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
  - [User Registration](#user-registration)
  - [User Login](#user-login)
  - [Retrieve User Profiles](#retrieve-user-profiles)
  - [Retrieve User Followers](#retrieve-user-followers)
  - [Retrieve User Following](#retrieve-user-following)
  - [Create User Relationship](#create-user-relationship)
  - [Delete User Relationship](#delete-user-relationship)

## Installation

Before using the "Users" app, you need to set it up in your Django project. Here are the steps for installation:

1. Clone the project repository:
```bash
git clone https://github.com/Yasu-Fadhili/knox_auth.git
```

2. Navigate to the project directory:
```bash
cd yourproject
```

3. Install the required Python packages using pip:
```bash
pip install -r requirements.txt
```

4. Run migrations to create the app's database tables:
```bash
python manage.py migrate
```

5. Run the development server:
```bash
python manage.py runserver
```

Your "Users" app is now installed and ready to use.

## Project Structure

Before setting up your project, make sure you have a basic understanding of its structure. The structure typically includes directories and files such as:

- `manage.py` - The Django management script.
- `yourproject/` - The main project directory.
  - `settings.py` - Django project settings.
  - `urls.py` - URL configuration.
  - `apps/` - Application directories.
  - `templates/` - HTML templates.
  - `static/` - Static files (CSS, JavaScript, etc.).
  - `requirements.txt` - Python package dependencies.

## Project Setup

1. **Create a Virtual Environment:**
   - If not already installed, install virtualenv:
     ```shell
     pip install virtualenv
     ```
   - Create a virtual environment for your project:
     ```shell
     virtualenv venv
     ```
   - Activate the virtual environment:
     - On Windows:
       ```shell
       venv\Scripts\activate
       ```
     - On macOS and Linux:
       ```shell
       source venv/bin/activate
       ```
2. **Install Django and Required Packages:**
   - Install Django and other necessary packages in your virtual environment:
     ```shell
     pip install -r requirements.txt
     ```

3. **Create a Django Project:**
   - Create a new Django project using the following command:
     ```shell
     django-admin startproject yourproject
     ```

## Django Settings

1. **Configure Installed Apps:**
   - In `yourproject/settings.py`, add the following apps to the `INSTALLED_APPS` list:
     ```python
     INSTALLED_APPS = [
         # ...
         'rest_framework',
         'knox',
         'django_countries',
         'django_countries_plus',
         'allauth',
         'allauth.account',
         'allauth.socialaccount',
     ]
     ```

2. **Database Configuration:**
   - Configure your database settings in the `DATABASES` section of `settings.py`.
   - For example, you can use SQLite for development:
     ```python
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.sqlite3',
             'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
         }
     }
     ```

3. **Django Rest Framework and Knox:**
   - Configure Django Rest Framework and Knox settings:
     ```python
     REST_FRAMEWORK = {
         'DEFAULT_AUTHENTICATION_CLASSES': [
             'knox.auth.TokenAuthentication',
         ],
     }

     AUTHENTICATION_CLASSES = (
         'knox.auth.TokenAuthentication',
     )

     AUTH_USER_MODEL = 'users.User'  # Replace 'users' with your user app's name
     ```

4. **Internationalization and Localization:**
   - Configure the use of [Django Countries](https://github.com/SmileyChris/django-countries) and localization in `settings.py`:
     ```python
     COUNTRIES_OVERRIDE = {
         'UK': 'United Kingdom',
     }

     LANGUAGE_CODE = 'en-gb'
     TIME_ZONE = 'UTC'
     USE_I18N = True
     USE_L10N = True
     USE_TZ = True
     ```

   - Refer to [Django Countries](https://github.com/SmileyChris/django-countries) for More 


## URL Configuration

1. **Create URL Patterns:**
   - In `yourproject/urls.py`, create URL patterns for your project. For example:
     ```python
     from django.contrib import admin
     from django.urls import path, include

     urlpatterns = [
         path('admin/', admin.site.urls),
         path('users/', include('users.urls')),  # Include your app's URLs here
     ]
     ```



The "Users" app is structured as follows:

- `users/` - The main app directory.
- `__init__.py` - Initiates the users directory as a module
- `admin.py` - Defines the app's admin interface.
- `apps.py` - .
- `forms.py` - .
- `managers.py` - .
- `signals.py` - Handles the auto creation of Profile adn Profile Status on User creation.
- `tests.py` - .
- `models.py` - Defines the app's data models.
- `serializers.py` - Contains serializers for data serialization.
- `views.py` - Includes views for handling HTTP requests.
- `urls.py` - Configures URL routing for the app.

## API Endpoints

The "Users" app provides the following API endpoints, accessible from the base path `/users`.

### User Registration

- **Endpoint**: `/register/`
- **HTTP Method**: POST
- **Description**: Register a new user.
- **Request Body**: JSON with user information, including username, phone number, email, first name, and password.
- **Response**: Returns user information upon successful registration.
- **Permissions**: Open to all users.

### User Login

- **Endpoint**: `/login/`
- **HTTP Method**: POST
- **Description**: Authenticate and log in a user.
- **Request Body**: JSON with user credentials (phone number/username/email and password).
- **Response**: Returns an authentication token upon successful login.
- **Permissions**: Open to all users.

### Retrieve User Profiles

- **Endpoint**: `/<user_id>/profile/`
- **HTTP Method**: GET
- **Description**: Retrieve the profile of a specific user by their user ID.
- **Response**: Returns user profile information.
- **Permissions**: Open to all users.

### Retrieve User Followers

- **Endpoint**: `/<user_id>/followers/`
- **HTTP Method**: GET
- **Description**: Retrieve the list of followers of a specific user by their user ID.
- **Response**: Returns a list of followers' information.
- **Permissions**: Open to all users.

### Retrieve User Following

- **Endpoint**: `/<user_id>/following/`
- **HTTP Method**: GET
- **Description**: Retrieve the list of users followed by a specific user by their user ID.
- **Response**: Returns a list of users being followed.
- **Permissions**: Open to all users.

### Create User Relationship

- **Endpoint**: `/relationship/create/`
- **HTTP Method**: POST
- **Description**: Create a new user relationship (e.g., follow another user).
- **Request Body**: JSON with the ID of the user to be followed.
- **Response**: Returns the created relationship information.
- **Permissions**: Open to all users.

### Delete User Relationship

- **Endpoint**: `/relationship/delete/<following_id>/`
- **HTTP Method**: DELETE
- **Description**: Delete a user relationship (e.g., unfollow another user) by specifying the user to unfollow.
- **Response**: No content response upon successful deletion.
- **Permissions**: Open to all users.

This documentation provides an overview of the "Users" app, its functionality, and API endpoints. Use the provided API endpoints to interact with user-related data within your Django project.

## Conclusion

The "Users" app is a tool for user management and social interactions within your application. Feel free to explore and customise the app to suit your project's specific requirements.

This documentation serves as a reference guide for working with the "Users" app and its endpoints. If you have any questions or need further assistance, please refer to the project's [Readme.MD](https://github.com/Yasu-Fadhili/knox_auth/blob/master/README.md) File or reach out to me - [Yasu Fadhili](https://github.com/Yasu-Fadhili).

Happy coding!


