

# Django Auth App

This Django Auth boilerplate provides basic authentication, OTP verification, and role-based access control for admin and customer users.

## Features

- User registration with OTP verification
- Password reset with OTP
- Role-based access control (Customer and Admin)
- Swagger API documentation for easy API management and testing

## Installation

1. Install the package:

   ```bash
   pip install django-auth-app
   ```

2. Add `auth_app` to your `INSTALLED_APPS` in Django settings:

   ```python
   # settings.py
   INSTALLED_APPS = [
       ...
       'auth_app',
       ...
   ]
   ```

3. Include the URLs in your `urls.py`:

   ```python
   # urls.py
   from django.urls import path, include

   urlpatterns = [
       path('auth/', include('auth_app.urls')),
   ]
   ```

4. Run migrations to create the necessary models:

   ```bash
   python manage.py migrate
   ```

## Usage

This boilerplate includes user registration and authentication features out of the box. Role-based access control is applied to differentiate between admin and customer users. Use Swagger API documentation to explore the available endpoints.

## License

This project is licensed under the MIT License.

