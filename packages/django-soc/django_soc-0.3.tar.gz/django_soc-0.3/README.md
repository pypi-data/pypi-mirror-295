# Django User Log

## Overview
Django User Log is a Django application designed to log user activities, including their IP address, country, and the full path of the pages they visit. This can be useful for analytics, security, and monitoring purposes.

## Features
- Logs user IP addresses
- Logs user countries
- Logs the full path with the host of visited pages
- Stores logs in the database for easy retrieval and analysis

## Installation
1. Clone the repository:
    ```sh
    git clone <repository-url>
    ```
2. Navigate to the project directory:
    ```sh
    cd django-userlog
    ```
3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```
4. Apply migrations:
    ```sh
    python manage.py makemigrations userlog
    python manage.py migrate
    ```

## Usage
1. Add the `userlog` app to your `INSTALLED_APPS` in `settings.py`:
    ```python
    INSTALLED_APPS = [
        ...
        'userlog',
    ]
    ```
2. Include the middleware in your `MIDDLEWARE` settings:
    ```python
    MIDDLEWARE = [
        ...
        'userlog.middleware.UserLogMiddleware',
    ]
    ```

