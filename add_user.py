import airflow
from airflow import models, settings
from airflow.contrib.auth.backends.password_auth import PasswordUser
from sqlalchemy import create_engine

user = PasswordUser(models.User())
user.username = ''
user.email = ''
user.password = ''

# Make the value true if you want the user to be a administrator
user.superuser = False

engine = create_engine("postgresql://airflow:airflow@postgres:5432/airflow")
session = settings.Session(bind=engine)
session.add(user)
session.commit()
session.close()
exit()