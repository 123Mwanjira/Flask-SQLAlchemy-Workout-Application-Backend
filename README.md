# Flask SQLAlchemy Workout Application Backend

A RESTful backend API for managing workouts, exercises, and the relationship between workouts and exercises. The application is built with Flask, Flask-SQLAlchemy, Flask-Migrate, Marshmallow, and SQLite.

## Features

* Create and retrieve exercises
* Retrieve an individual exercise
* Update an exercise using PATCH
* Delete an exercise
* Create and retrieve workouts
* Retrieve a workout together with its exercises
* Add exercises to workouts
* Marshmallow serialization and schema validation
* SQLAlchemy model validations
* Database-level table constraints
* Database migrations using Flask-Migrate
* Seed data for exercises, workouts, and workout exercises

## Technologies Used

* Python 3.8.13
* Flask 2.2.2
* Flask-SQLAlchemy 3.0.3
* Flask-Migrate 3.1.0
* Marshmallow 3.20.1
* SQLite
* Pipenv
* Alembic

## Project Structure

```text
Flask-SQLAlchemy-Workout-Application-Backend/
├── migrations/
│   ├── versions/
│   ├── env.py
│   ├── alembic.ini
│   └── script.py.mako
├── server/
│   ├── app.py
│   ├── models.py
│   ├── schemas.py
│   └── seed.py
├── Pipfile
├── Pipfile.lock
└── README.md
```

## Installation

Clone the repository and enter the project directory:

```bash
git clone https://github.com/123Mwanjira/Flask-SQLAlchemy-Workout-Application-Backend.git
cd Flask-SQLAlchemy-Workout-Application-Backend
```

Install the project dependencies using Pipenv:

```bash
pipenv install
```

Activate the virtual environment:

```bash
pipenv shell
```

Set the Flask application:

```bash
export FLASK_APP=server/app.py
```

## Database Setup

Apply the existing database migrations:

```bash
flask db upgrade
```

To check the current migration:

```bash
flask db current
```

The application should report the current migration revision.

## Seed the Database

Populate the database with starter data:

```bash
python server/seed.py
```

The seed file creates starter records for exercises, workouts, and workout exercises.

## Running the Application

Start the Flask development server:

```bash
flask run --port 5555
```

The API will be available at:

```text
http://127.0.0.1:5555
```

Alternatively, the application can be started directly with:

```bash
python server/app.py
```

## API Endpoints

### Exercises

| Method | Endpoint                   | Description        |
| ------ | -------------------------- | ------------------ |
| GET    | `/exercises`               | Get all exercises  |
| POST   | `/exercises`               | Create an exercise |
| GET    | `/exercises/<exercise_id>` | Get one exercise   |
| PATCH  | `/exercises/<exercise_id>` | Update an exercise |
| DELETE | `/exercises/<exercise_id>` | Delete an exercise |

### Workouts

| Method | Endpoint                 | Description                        |
| ------ | ------------------------ | ---------------------------------- |
| GET    | `/workouts`              | Get all workouts                   |
| POST   | `/workouts`              | Create a workout                   |
| GET    | `/workouts/<workout_id>` | Get one workout with its exercises |

### Workout Exercises

| Method | Endpoint                           | Description                  |
| ------ | ---------------------------------- | ---------------------------- |
| POST   | `/workouts/<workout_id>/exercises` | Add an exercise to a workout |

## Example Requests

Create an exercise:

```bash
curl -X POST http://127.0.0.1:5555/exercises \
-H "Content-Type: application/json" \
-d '{"name":"Bench Press","category":"Strength","equipment_needed":true}'
```

Create a workout:

```bash
curl -X POST http://127.0.0.1:5555/workouts \
-H "Content-Type: application/json" \
-d '{"date":"2026-08-30","duration_minutes":60,"notes":"Evening workout"}'
```

Add an exercise to a workout:

```bash
curl -X POST http://127.0.0.1:5555/workouts/1/exercises \
-H "Content-Type: application/json" \
-d '{"exercise_id":1,"reps":10,"sets":3}'
```

Get a workout with its exercises:

```bash
curl http://127.0.0.1:5555/workouts/1
```

## Validation

The application uses Marshmallow schema validation to ensure that incoming data meets the required rules.

Examples include:

* Exercise names cannot be empty.
* Exercise categories are required.
* Workout dates are required.
* Workout duration must be at least 1 minute.
* Repetitions cannot be negative.
* Sets cannot be negative.
* Exercise duration cannot be negative.

The application also uses SQLAlchemy model validations and database-level `CheckConstraint`s to protect data integrity.

## Database Migrations

Flask-Migrate is used to manage database schema changes.

Create a new migration after changing the models:

```bash
flask db migrate -m "describe the change"
```

Apply migrations:

```bash
flask db upgrade
```

Check the current migration:

```bash
flask db current
```

## Git Workflow

The project uses feature branches and meaningful commits. The current development branch is:

```text
feature/setup
```

Changes are committed regularly and pushed to the remote repository.

## Author

Maurine Gichuhi
