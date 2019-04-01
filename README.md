# Portal Stack

[![Python Version](https://img.shields.io/badge/python-3.6-brightgreen.svg)](https://python.org)
[![Django Version](https://img.shields.io/badge/django-2.0-brightgreen.svg)](https://djangoproject.com)

This project is about making a Training & Placement portal system for Students & T.P head to get access for the notices and other information that is uploaded by their T.P head. 


## Running the Project Locally

First, clone the repository to your local machine:

```bash
git clone https://github.com/vedantv/portal_stack.git
```

Install the requirements:

```bash
pip install -r requirements.txt
```

Create the database:

```bash
python manage.py migrate
```

Finally, run the development server:

```bash
python manage.py runserver
```

The project will be available at **127.0.0.1:8000**.

# References

Read the blog post [How to Implement Multiple User Types with Django](https://simpleisbetterthancomplex.com/tutorial/2018/01/18/how-to-implement-multiple-user-types-with-django.html).