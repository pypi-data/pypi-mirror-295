

# django-auth-app

A Django authentication boilerplate with OTP and role-based access control. This package provides a robust and reusable authentication system, including basic registration, login/logout, password management, OTP setup, email verification, and social authentication integration.

## Features

- **Basic Authentication**: Registration, login, logout, password change.
- **OTP Verification**: For registration and password reset.
- **Email Verification**: Through SMTP.
- **Social Authentication**: Google and Facebook integration.
- **Role-Based Access Control (RBAC)**: Differentiated roles for custom and social registrations.
- **Swagger Documentation**: API documentation.
- **JWT Token Authentication**: For API access.

## Installation

1. **Install the package**:
   
   ```bash
   pip install django-auth-app
   ```

2. **Add the app to your Django project**:

   In your `settings.py`, add `auth_app` to your `INSTALLED_APPS`:

   ```python
   INSTALLED_APPS = [
       # Other installed apps
       'auth_app',
       'rest_framework',
       'drf_yasg',
       
   ]
   ```

3. **Configure SMTP for email sending**:

   Add your SMTP settings to `settings.py`:

   ```python
   EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
   EMAIL_HOST = 'smtp.example.com'
   EMAIL_PORT = 587
   EMAIL_USE_TLS = True
   EMAIL_HOST_USER = 'your_email@example.com'
   EMAIL_HOST_PASSWORD = 'your_email_password'
   ```

4. **Set up JWT authentication**:

   Add the following to `settings.py`:

   ```python
   REST_FRAMEWORK = {
       'DEFAULT_AUTHENTICATION_CLASSES': [
           'rest_framework_simplejwt.authentication.JWTAuthentication',
       ],
   }
   ```

5. **Include the URL configurations**:

   Add the following to your project's `urls.py`:

   ```python
   from django.urls import path, include
   from auth_app import views

   urlpatterns = [
       path('auth/', include('auth_app.urls')),
       # Other URLs
   ]
   ```

8. **Run migrations**:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

## Usage

### Web Views

- **Registration**: `/register/`
- **Login**: `/login/`
- **Logout**: `/logout/`
- **Password Change**: `/password-change/`
- **Password Reset**: `/password-reset/`
- **OTP Verification**: `/otp-verify/`

### API Endpoints

- **Register**: `api/register/`
- **Login**: `api/login/`
- **OTP Verify**: `api/otp-verify/`
- **Password Change**: `api/password-change/`
- **Password Reset**: `api/password-reset/`

### Swagger Documentation

- **Swagger UI**: `/docs/`

## Development

To contribute to the development of `django-auth-app`, clone the repository and install the dependencies:

```bash
git clone https://github.com/sajan69/django-auth-boilerplate.git
cd django-auth-boilerplate
pip install -r requirements.txt
```

## Testing

To run tests, use:

```bash
pytest
```

## License

MIT License. See the [LICENSE](https://github.com/sajan69/django-auth-boilerplate/blob/main/LICENSE) file for details.

## Author

Sajan Adhikari  
[sajana46@gmail.com](mailto:sajana46@gmail.com)

---