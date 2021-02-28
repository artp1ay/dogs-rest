## About

Test project to demonstrate CRUD capabilities in the Django REST Framework using a dog breed database as an example. In
the application, you can create new breeds and add dogs. The project runs on PostgreSQL or SQLite3 if Postgre data is
not specified in ENV. The project can be run using Docker.

## Used Stack

- Python
- Django
- Django REST Framework
- Docker
- PostgreSQL or SQLite3
- Gunicorn

## Available Methods

| Endpoint | Request Type | Description |
| :--- | :--- | :--- | 
| api/v1/dogs/ | GET, POST  | Get a list of all dogs, add a new dog, or search by dog name |
| api/v1/dogs/{dog_id}/ | GET, PUT, DELETE  | Retrieving, deleting, partial/full editing of dog data by id |
| api/v1/breeds/ | GET, POST  | Get a list of all dog breeds or add a new breed |
| api/v1/breed/{breed_id}/ | GET, PUT, DELETE  | Retrieving, deleting, partial / full editing of breed data by id |

## Examples

All API endpoints return a JSON representation of received, created or edited objects.

Example of a response to a request GET api/v1/dogs/{dog_id}/

    {
        "name": "Bobby",
        "sex": "Male",
        "coat_color": "black",
        "behavior": "calm",
        "breed": "Labrador Retreiver",
        "age": 3
    }

Example of a POST request to api/v1/dogs/

    {
        "name": "Jessy",
        "sex": "Female",
        "coat_color": "brown",
        "behavior": "Aggressive",
        "breed": "Setter",
        "age": 5
    }

In the behavior field, you can enter names from the list: Aggressive, Calm, Playful In the sex field, you can enter
names from the list: Male, Female By default, both fields will be filled with the value "Unknown"

## How to run

### Setup

1. Clone repository to your local computer, simply run:
   ```
   git clone https://github.com/artplay/dogs-rest
   ```
2. In the root directory, edit the file `.env_example` and rename it to `.env`. You can generate new secret
   key [here](https://ya.ru):
    ```
    SECRET_KEY='YOUR KEY HERE'
    DB_ENGINE=django.db.backends.postgresql
    DB_NAME=postgres
    DB_USER=postgres
    DB_PASSWORD=postgres
    DB_HOST=db
    DB_PORT=5432
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    ```

### Docker

In order to run the application via docker, just run the command:

```
docker-compose up
```

To make migrations run:

```
docker exec -it <container id> bash
python manage.py makemigrations
python manage.py migrate
```

    
    
    
    
    
