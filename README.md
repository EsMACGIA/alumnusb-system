# ALUMNUSB-SYSTEM
Web application using gamification strategies for the AlumnUSB NGO. It seeks to 
motivate graduates of the Simón Bolívar University to make donations constantly 
through a medal system. In addition, the application allows you to view user 
statistics.

#
Software and versions
---------

- Python: 3.6.12
- PIP: 20.3.3
- Postgres: 13.1
- Docker: 19.03.8

#
Requirements to run
---------

- Python (>=3.x <3.8.x)

## How to run the application

### Running with Docker Compose

To execute the app with __Docker Composer__ simply execute `docker-compose up` 
in the root of the project. This will create and execute 2 containers: 1 with an 
instance of a PostgreSQL DB and one with the API created with Django.

To check if it is working just go to http://localhost:8000/ in your web browser.

**Note1:** Ports `8000` and `5432` should be available in your local machine in 
order to bind the __Docker__ containers to your machine ports.

**Note2**: If you need to erase the data on the database delete the postgres 
container with the following command and compose after it: 
```
$ docker container rm alumnusb-system_db_1
```
