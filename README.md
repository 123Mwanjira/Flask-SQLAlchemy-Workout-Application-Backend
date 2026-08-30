# Flask SQLAlchemy Workout Application Backend

A RESTful backend API for a workout tracking application used by personal trainers. The application manages reusable exercises, workouts, and the relationship between workouts and exercises.

The backend is built with Flask, Flask-SQLAlchemy, Flask-Migrate, Marshmallow, SQLite, and Pipenv.

## Features

* Create, view, update, and delete exercises
* Create, view, and delete workouts
* Add exercises to workouts
* View an exercise together with its associated workouts
* View a workout together with its associated exercises
* Store reps, sets, and duration for exercises within workouts
* Marshmallow serialization and deserialization
* Marshmallow schema validation
* SQLAlchemy model-level validation
* Database-level table constraints
* Foreign-key relationships between models
* Database migrations using Flask-Migrate and Alembic
* Seed data for exercises, workouts, and workout exercises
* Clean separation of models, schemas, application routes, and seed data

## Technologies Used

* Python 3.8.13
* Flask 2.2.2
* Flask-SQLAlchemy 3.0.3
* Flask-Migrate 3.1.0
* Marshmallow 3.20.1
* SQLite
* Pipenv
* Alembic
* Git and GitHub

## Project Structure

text
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
├── README.md
└── .gitignore
```

## Installation

Clone the repository:

```bash
git clone https://github.com/123Mwanjira/Flask-SQLAlchemy-Workout-Application-Backend.git
cd Flask-SQLAlchemy-Workout-Application-Backend


Install the project dependencies using Pipenv:

bash
pipenv install


Activate the virtual environment:

bash
pipenv shell


Set the Flask application:

bash
export FLASK_APP=server/app.py


## Database Setup

Apply the existing database migration:

bash
flask db upgrade


Check the current migration:

bash
flask db current


The database should report the current migration revision.

To create a new migration after making model changes:

bash
flask db migrate -m "describe the change"


Then apply it:

bash
flask db upgrade


## Seed the Database

The project includes a seed file that creates starter records for all three models:

* Exercises
* Workouts
* WorkoutExercises

Run:

bash
python server/seed.py


The seed file clears existing workout-exercise, workout, and exercise records before creating the starter data. This allows the database to be reset and reseeded without creating duplicate starter records.

Expected output:

text
Database seeded successfully!


## Running the Application

Start the Flask development server:

bash
flask run --port 5555


The API will be available at:

text
http://127.0.0.1:5555

Alternatively, the application can be started directly with:

bash
python server/app.py


## Data Models

### Exercise

| Field              | Type    | Description                   |
| ------------------ | ------- | ----------------------------- |
| `id`               | Integer | Primary key                   |
| `name`             | String  | Exercise name                 |
| `category`         | String  | Exercise category             |
| `equipment_needed` | Boolean | Whether equipment is required |

### Workout

| Field              | Type    | Description            |
| ------------------ | ------- | ---------------------- |
| `id`               | Integer | Primary key            |
| `date`             | Date    | Workout date           |
| `duration_minutes` | Integer | Workout duration       |
| `notes`            | Text    | Optional workout notes |

### WorkoutExercise

| Field              | Type    | Description                  |
| ------------------ | ------- | ---------------------------- |
| `id`               | Integer | Primary key                  |
| `workout_id`       | Integer | Foreign key to Workout       |
| `exercise_id`      | Integer | Foreign key to Exercise      |
| `reps`             | Integer | Number of repetitions        |
| `sets`             | Integer | Number of sets               |
| `duration_seconds` | Integer | Exercise duration in seconds |

## Relationships

The application implements the following relationships:

* A `WorkoutExercise` belongs to a `Workout`.
* A `WorkoutExercise` belongs to an `Exercise`.
* A `Workout` has many `WorkoutExercises`.
* An `Exercise` has many `WorkoutExercises`.
* A `Workout` has many `Exercises` through `WorkoutExercises`.
* An `Exercise` has many `Workouts` through `WorkoutExercises`.

## API Endpoints

### Exercises

| Method | Endpoint                   | Description                                  |
| ------ | -------------------------- | -------------------------------------------- |
| GET    | `/exercises`               | List all exercises                           |
| GET    | `/exercises/<exercise_id>` | Show an exercise and its associated workouts |
| POST   | `/exercises`               | Create an exercise                           |
| PATCH  | `/exercises/<exercise_id>` | Update an exercise                           |
| DELETE | `/exercises/<exercise_id>` | Delete an exercise                           |

### Workouts

| Method | Endpoint                 | Description                                 |
| ------ | ------------------------ | ------------------------------------------- |
| GET    | `/workouts`              | List all workouts                           |
| GET    | `/workouts/<workout_id>` | Show a workout and its associated exercises |
| POST   | `/workouts`              | Create a workout                            |
| DELETE | `/workouts/<workout_id>` | Delete a workout                            |

### Workout Exercises

| Method | Endpoint                                                           | Description                                                   |
| ------ | ------------------------------------------------------------------ | ------------------------------------------------------------- |
| POST   | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add an exercise to a workout with reps, sets, and/or duration |

## Example Requests

### Create an Exercise

```bash
curl -X POST http://127.0.0.1:5555/exercises \
-H "Content-Type: application/json" \
-d '{"name":"Bench Press","category":"Strength","equipment_needed":true}'


### Create a Workout

```bash
curl -X POST http://127.0.0.1:5555/workouts \
-H "Content-Type: application/json" \
-d '{"date":"2026-08-30","duration_minutes":60,"notes":"Evening workout"}'


### Add an Exercise to a Workout

bash
curl -X POST http://127.0.0.1:5555/workouts/1/exercises/2/workout_exercises \
-H "Content-Type: application/json" \
-d '{"reps":12,"sets":3}'


### Get All Exercises

bash
curl http://127.0.0.1:5555/exercises


### Get One Exercise with Associated Workouts

bash
curl http://127.0.0.1:5555/exercises/1


### Get All Workouts

bash
curl http://127.0.0.1:5555/workouts


### Get One Workout with Associated Exercises

bash
curl http://127.0.0.1:5555/workouts/1


### Delete an Exercise
bash
curl -X DELETE http://127.0.0.1:5555/exercises/1


### Delete a Workout

bash
curl -X DELETE http://127.0.0.1:5555/workouts/1


## Validation

The application validates data at multiple levels.

### Schema Validations

Marshmallow validates incoming API requests.

Examples include:

* Exercise `name` is required and cannot be empty.
* Exercise `category` is required and cannot be empty.
* `equipment_needed` must be a boolean.
* Workout `date` is required.
* Workout `duration_minutes` must be at least 1.
* `reps` cannot be negative.
* `sets` cannot be negative.
* `duration_seconds` cannot be negative.

Invalid input returns a `400 Bad Request` response containing validation errors.

### Model Validations

SQLAlchemy model validators provide additional protection against invalid data.

Examples include:

* Exercise names cannot be empty.
* Exercise categories cannot be empty.
* Workout duration must be greater than zero.
* Repetitions cannot be negative.
* Sets cannot be negative.
* Exercise duration cannot be negative.

### Database Table Constraints

Database-level `CheckConstraint`s provide an additional layer of data integrity.

The database enforces constraints including:

* Exercise names cannot contain only whitespace.
* Exercise categories cannot contain only whitespace.
* Workout duration must be greater than zero.
* Repetitions must be non-negative when provided.
* Sets must be non-negative when provided.
* Exercise duration must be non-negative when provided.

## Error Handling

The API returns appropriate HTTP status codes for common situations.

Examples:

* `200 OK` — Successful GET, PATCH, or DELETE operation.
* `201 Created` — Successfully created a new resource.
* `400 Bad Request` — Invalid request data.
* `404 Not Found` — Requested workout or exercise does not exist.

Example:

```json
{
  "error": "Exercise not found"
}
```

## Database Migrations

Flask-Migrate and Alembic are used to manage database schema changes.

Current migration can be checked with:

```bash
flask db current
```

The existing migration creates:

* `exercises`
* `workouts`
* `workout_exercises`

The migration also includes the database-level validation constraints.

## Git Workflow

The project uses Git feature branches and meaningful commits.

Development was completed on:

```text
feature/setup
```

Changes were committed and pushed regularly to GitHub.

The final completed version should be merged into the `main` branch for submission.

## Author

Maurine Gichuhi
