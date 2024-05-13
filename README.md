# DBMS
Campus Event Management System

## Get started
Run all of this inside `src` directory

### Python packages
Run this command to install all required packages
`pip install -r requirements.txt`

### Database

Set your password in `src/CEMS/settings.py` under DATABASES-PASSWORD (do not commit this change).
Replace 'PASSWORD' with your own mysql server password.

Start with a fresh database my opening your mysql server and use
`create database CEMS;`
(Delete the CEMS database if you made it before).

Use this command to create all the necessary tables we need in our database
`python manage.py migrate`

We need django to manage our database we shouldnt be doing it manually.
All models are linked to the tables we need in our mysql database.