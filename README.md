# Bank Web App

## Project Overview

The Bank Web App is a sample application that can be used to mock a banking application. With it, you can create an account, make deposits, withdraws, and transfers, and delete accounts among other things.

## Running

To run the project, navigate to the `/bank-web-app/bank_project` directory and run the following:

```
python manage.py runserver
```

By default, the development server runs on `localhost:8000`. The port can be changed using the following command:

```
python manage.py runserver 8080
```

The IP address can be configured using the following command:

```
python manage.py runserver 0.0.0.0:8000
```

## Database

The banking application is backed by a SQLite database. In the future, we plan on migrating to PostgreSQL.
