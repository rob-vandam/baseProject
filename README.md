#Example Fastapi app for Camping.care

This is a basic example of a Fastapi app to download some data from Camping.care and store this to a .csv file

This programm is free to use and distribute.

##To get started:

Install the requirements from requirements.txt

Run the Alembic migration:
alembic upgrade head

Start the development server:
uvicorn app.main:app --reload

Install the app in Camping.care:

App url:
http://127.0.0.1:8000

Widget url:
http://localhost:8000/get_csv

Scopes:
reservations.list
