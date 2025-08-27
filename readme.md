Backend
This is the backend for the Nynx Creatives project, built with Django and integrated with Celery, Redis, AWS S3, Stripe, PayPal, Payoneer, and Zendesk.


Requirements
Python 3.8+
pip
Redis
AWS S3 bucket
Django
Celery
Django Storages
Stripe, PayPal, Payoneer accounts
Setup
Clone the repository:


git clone <repo-url>
cd Backend
Create a virtual environment:


python -m venv venv
source venv/bin/activate
Install dependencies:


pip install -r requirements.txt
Configure environment variables:


Copy .env.example to .env and fill in your credentials.
Apply migrations:


python manage.py makemigrations
python manage.py migrate
Collect static files:


python manage.py collectstatic
Running
Start Django server:


python manage.py runserver
Start Celery worker:


celery -A <your_project_name> worker -l info
Start Celery beat:


celery -A <your_project_name> beat -l info
Integrations
AWS S3: Used for media file storage.
Redis: Used as Celery broker.
Stripe, PayPal, Payoneer: Payment processing.
Zendesk: Customer support integration.
Environment Variables
See .env for all required variables (database, email, payment, S3, etc.).


License
See LICENSE file for details.