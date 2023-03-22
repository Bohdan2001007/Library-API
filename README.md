# Library-API

API service that helps the library manage borrowings

# Features

- JWT authentication

- Swagger documentation

- Managing books and borrowings

- Filtering borrowing by active borrowing (is_active) and user_id (admin only)

# Installing

- git clone git@github.com:Bohdan2001007/Library-API.git
cd Library-API
python -m venv venv
sourve venv/bin/activate
pip install -r requirements.txt

# Run locally

- python manage.py migrate

- python manage.py runserver

Access

- api/user/register

- get access token via api//user/token/

Secret Key

- create your own .env file and store your own secret key here, like in .env_sample
