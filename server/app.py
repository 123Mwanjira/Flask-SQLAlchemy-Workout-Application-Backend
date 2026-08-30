
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from marshmallow import ValidationError

from models import db, Exercise, Workout, WorkoutExercise
from schemas import ExerciseSchema, WorkoutSchema, WorkoutExerciseSchema


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)


# --------------------------------------------------
# Schemas
# --------------------------------------------------

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

workout_exercise_schema = WorkoutExerciseSchema()


# --------------------------------------------------
# GET all exercises
# --------------------------------------------------

@app.route("/exercises", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.all()

    return jsonify(exercises_schema.dump(exercises))


# --------------------------------------------------
# CREATE an exercise
# --------------------------------------------------

@app.route("/exercises", methods=["POST"])
def create_exercise():
    data = request.get_json()

    try:
        validated_data = exercise_schema.load(data)
    except ValidationError as error:
        return jsonify({"error": error.messages}), 400

    exercise = Exercise(
        name=validated_data["name"],
        category=validated_data["category"],
        equipment_needed=validated_data["equipment_needed"]
    )

    try:
        db.session.add(exercise)
        db.session.commit()
    except ValueError as error:
        db.session.rollback()
        return jsonify({"error": str(error)}), 400

    return jsonify(exercise_schema.dump(exercise)), 201


# --------------------------------------------------
# GET one exercise
# --------------------------------------------------

@app.route("/exercises/<int:exercise_id>", methods=["GET"])
def get_exercise(exercise_id):
    exercise = db.session.get(Exercise, exercise_id)

    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404

    return jsonify(exercise_schema.dump(exercise))


# --------------------------------------------------
# UPDATE an exercise
# --------------------------------------------------

@app.route("/exercises/<int:exercise_id>", methods=["PATCH"])
def update_exercise(exercise_id):
    exercise = db.session.get(Exercise, exercise_id)

    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404

    data = request.get_json()

    try:
        validated_data = exercise_schema.load(
            data,
            partial=True
        )
    except ValidationError as error:
        return jsonify({"error": error.messages}), 400

    try:
        if "name" in validated_data:
            exercise.name = validated_data["name"]

        if "category" in validated_data:
            exercise.category = validated_data["category"]

        if "equipment_needed" in validated_data:
            exercise.equipment_needed = validated_data["equipment_needed"]

        db.session.commit()

    except ValueError as error:
        db.session.rollback()
        return jsonify({"error": str(error)}), 400

    return jsonify(exercise_schema.dump(exercise))


# --------------------------------------------------
# DELETE an exercise
# --------------------------------------------------

@app.route("/exercises/<int:exercise_id>", methods=["DELETE"])
def delete_exercise(exercise_id):
    exercise = db.session.get(Exercise, exercise_id)

    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404

    db.session.delete(exercise)
    db.session.commit()

    return jsonify({"message": "Exercise deleted successfully"})


# --------------------------------------------------
# GET all workouts
# --------------------------------------------------

@app.route("/workouts", methods=["GET"])
def get_workouts():
    workouts = Workout.query.all()

    return jsonify(workouts_schema.dump(workouts))


# --------------------------------------------------
# CREATE a workout
# --------------------------------------------------

@app.route("/workouts", methods=["POST"])
def create_workout():
    data = request.get_json()

    try:
        validated_data = workout_schema.load(data)
    except ValidationError as error:
        return jsonify({"error": error.messages}), 400

    workout = Workout(
        date=validated_data["date"],
        duration_minutes=validated_data["duration_minutes"],
        notes=validated_data.get("notes")
    )

    try:
        db.session.add(workout)
        db.session.commit()
    except ValueError as error:
        db.session.rollback()
        return jsonify({"error": str(error)}), 400

    return jsonify(workout_schema.dump(workout)), 201


# --------------------------------------------------
# GET one workout with its exercises
# --------------------------------------------------

@app.route("/workouts/<int:workout_id>", methods=["GET"])
def get_workout(workout_id):
    workout = db.session.get(Workout, workout_id)

    if not workout:
        return jsonify({"error": "Workout not found"}), 404

    result = workout_schema.dump(workout)

    result["exercises"] = [
        {
            "id": workout_exercise.exercise.id,
            "name": workout_exercise.exercise.name,
            "category": workout_exercise.exercise.category,
            "equipment_needed": workout_exercise.exercise.equipment_needed,
            "reps": workout_exercise.reps,
            "sets": workout_exercise.sets,
            "duration_seconds": workout_exercise.duration_seconds
        }
        for workout_exercise in workout.workout_exercises
    ]

    return jsonify(result)


# --------------------------------------------------
# ADD an exercise to a workout
# --------------------------------------------------

@app.route(
    "/workouts/<int:workout_id>/exercises",
    methods=["POST"]
)
def add_exercise_to_workout(workout_id):
    data = request.get_json()

    workout = db.session.get(Workout, workout_id)

    if not workout:
        return jsonify({"error": "Workout not found"}), 404

    try:
        validated_data = workout_exercise_schema.load(data)
    except ValidationError as error:
        return jsonify({"error": error.messages}), 400

    exercise = db.session.get(
        Exercise,
        validated_data["exercise_id"]
    )

    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404

    workout_exercise = WorkoutExercise(
        workout_id=workout.id,
        exercise_id=exercise.id,
        reps=validated_data.get("reps"),
        sets=validated_data.get("sets"),
        duration_seconds=validated_data.get("duration_seconds")
    )

    try:
        db.session.add(workout_exercise)
        db.session.commit()
    except ValueError as error:
        db.session.rollback()
        return jsonify({"error": str(error)}), 400

    return jsonify(
        workout_exercise_schema.dump(workout_exercise)
    ), 201


# --------------------------------------------------
# Start the application
# --------------------------------------------------

if __name__ == "__main__":
    app.run(port=5555, debug=True)