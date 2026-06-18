# Gustus

*My first attempt at building a deployment-ready Django application.*

Gustus is a food rating and recommendation web app. The idea came from a simple problem: sometimes we order food, get disappointed, forget about it, and later order from the same place again. Sometimes we do not know what to order, and delivery app recommendations are not very helpful. Sometimes we simply want to know just how much KFC we actually eat.

The goal of Gustus is to create a small "Spotify for food": an app that stores restaurant experiences, lets users rate places across different categories, keeps an eating-out history, and eventually recommends restaurants based on personal preferences.

For now, this project is being built as an MVP for my programming course final. The main focus is on Django, relational database design, CRUD, REST API, user accounts, and a simple recommendation/statistics layer.

## Installation

Clone the repository:

```bash
git clone https://github.com/InformaticusMaximus/gustus.git
cd gustus
```

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

On Windows use:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Apply database migrations:

```bash
python manage.py migrate
```

Create an admin user:

```bash
python manage.py createsuperuser
```

Run the development server:

```bash
python manage.py runserver
```

Open the application in the browser:

```text
http://127.0.0.1:8000/
```

Admin panel:

```text
http://127.0.0.1:8000/admin/
```

API root:

```text
http://127.0.0.1:8000/api/
```

**At this point in development, only admin can manage restaurants**

## MVP Scope

- Django web application
- SQLite relational database
- Django ORM models and migrations
- User accounts
- Restaurant database
- User-specific restaurant profiles, including aliases and notes
- Restaurant experience history
- Rating history
- Functional CRUD
- REST API with Django REST Framework
- Simple statistics, such as top-rated and most visited restaurants
- Basic recommendation logic
- Simple responsive frontend

## Planned Features

- PostgreSQL database for production
- Google Places integration for restaurant identification and deduplication
- More advanced recommendation system
- Better frontend and user experience
- Extended account management
- Data backups
- Deployment on a custom domain

## Tech Stack

- Python
- Django
- Django REST Framework
- SQLite for local development
- HTML + CSS
- Git

## Current Status

Early MVP development.

The current focus is on building the relational data model, implementing CRUD operations, exposing a REST API, and preparing the basic web interface.
