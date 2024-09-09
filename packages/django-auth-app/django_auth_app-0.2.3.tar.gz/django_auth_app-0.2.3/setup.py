from setuptools import setup, find_packages

setup(
    name='django-auth-app',  # Your package name
    version='0.2.3',  # Version of your package
    packages=find_packages(),  # Automatically discover and include all packages
    include_package_data=True,  # Include static files like templates
    description='A Django authentication boilerplate with OTP and role-based access control',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # Specify the format of README
    url='https://github.com/sajan69/django-auth-boilerplate',  # URL of your project repository
    author='Sajan Adhikari',  # Your name as the author
    author_email='sajana46@gmail.com',  # Your email
    license='MIT',  # License type (MIT, BSD, GPL, etc.)
    classifiers=[  # Metadata for PyPI
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    install_requires=[
         'django>=3.0',
        'djangorestframework',
        'drf-yasg',  # For Swagger documentation
    ],
    python_requires='>=3.8',  # Specify supported Python versions
)
