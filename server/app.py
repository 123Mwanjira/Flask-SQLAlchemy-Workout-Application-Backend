from datetime import date

from flask import Flask, jsonify, request
from flask_migrate import Migrate

from models import db, Exercise, Workout, WorkoutExercise


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)


# --------------------------------------------------
# GET all exercises
# --------------------------------------------------
@app.route("/exercises", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.all()

    return jsonify([
        {
            "id": exercise.id,
            "name": exercise.name,
            "category": exercise.category,
            "equipment_needed": exercise.equipment_needed
        }
        for exercise in exercises
    ])


# --------------------------------------------------
# GET one exercise
# --------------------------------------------------
@app.route("/exercises/<int:exercise_id>", methods=["GET"])
def get_exercise(exercise_id):
    exercise = db.session.get(Exercise, exercise_id)

    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404

    return jsonify({
        "id": exercise.id,
        "name": exercise.name,
        "category": exercise.category,
        "equipment_needed": exercise.equipment_needed
    })


# --------------------------------------------------
# CREATE an exercise
# --------------------------------------------------
@app.route("/exercises", methods=["POST"])
def create_exercise():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    required_fields = ["name", "category", "equipment_needed"]

    for field in required_fields:
        if field not in data:
            return jsonify({
                "error": f"Missing required field: {field}"
            }), 400

    try:
        exercise = Exercise(
            name=data["name"],
            category=data["category"],
            equipment_needed=data["equipment_needed"]
        )

        db.session.add(exercise)
        db.session.commit()

    except ValueError as error:
        db.session.rollback()
        return jsonify({"error": str(error)}), 400

    return jsonify({
        "id": exercise.id,
        "name": exercise.name,
        "category": exercise.category,
        "equipment_needed": exercise.equipment_needed
    }), 201


# --------------------------------------------------
# UPDATE an exercise
# --------------------------------------------------
@app.route("/exercises/<int:exercise_id>", methods=["PATCH"])
def update_exercise(exercise_id):
    exercise = db.session.get(Exercise, exercise_id)

    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404

    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    try:
        if "name" in data:
            exercise.name = data["name"]

        if "category" in data:
            exercise.category = data["category"]

        if "equipment_needed" in data:
            exercise.equipment_needed = data["equipment_needed"]

        db.session.commit()

    except ValueError as error:
        db.session.rollback()
        return jsonify({"error": str(error)}), 400

    return jsonify({
        "id": exercise.id,
        "name": exercise.name,
        "category": exercise.category,
        "equipment_needed": exercise.equipment_needed
    })


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

    return jsonify({
        "message": "Exercise deleted successfully"
    })


# --------------------------------------------------
# GET all workouts
# --------------------------------------------------
@app.route("/workouts", methods=["GET"])
def get_workouts():
    workouts = Workout.query.all()

    return jsonify([
        {
            "id": workout.id,
            "date": workout.date.isoformat(),
            "duration_minutes": workout.duration_minutes,
            "notes": workout.notes
        }
        for workout in workouts
    ])


# --------------------------------------------------
# CREATE a workout
# --------------------------------------------------
@app.route("/workouts", methods=["POST"])
def create_workout():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    required_fields = ["date", "duration_minutes"]

    for field in required_fields:
        if field not in data:
            return jsonify({
                "error": f"Missing required field: {field}"
            }), 400

    try:
        workout = Workout(
            date=date.fromisoformat(data["date"]),
            duration_minutes=data["duration_minutes"],
            notes=data.get("notes")
        )

        db.session.add(workout)
        db.session.commit()

    except (ValueError, TypeError) as error:
        db.session.rollback()
        return jsonify({"error": str(error)}), 400

    return jsonify({
        "id": workout.id,
        "date": workout.date.isoformat(),
        "duration_minutes": workout.duration_minutes,
        "notes": workout.notes
    }), 201


# --------------------------------------------------
# GET one workout with its exercises
# --------------------------------------------------
@app.route("/workouts/<int:workout_id>", methods=["GET"])
def get_workout(workout_id):
    workout = db.session.get(Workout, workout_id)

    if not workout:
        return jsonify({"error": "Workout not found"}), 404

    return jsonify({
        "id": workout.id,
        "date": workout.date.isoformat(),
        "duration_minutes": workout.duration_minutes,
        "notes": workout.notes,
        "exercises": [
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
    })


# --------------------------------------------------
# ADD an exercise to a workout
# --------------------------------------------------
@app.route("/workouts/<int:workout_id>/exercises", methods=["POST"])
def add_exercise_to_workout(workout_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    if "exercise_id" not in data:
        return jsonify({"error": "exercise_id is required"}), 400

    workout = db.session.get(Workout, workout_id)

    if not workout:
        return jsonify({"error": "Workout not found"}), 404

    exercise = db.session.get(Exercise, data["exercise_id"])

    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404

    try:
        workout_exercise = WorkoutExercise(
            workout_id=workout.id,
            exercise_id=exercise.id,
            reps=data.get("reps"),
            sets=data.get("sets"),
            duration_seconds=data.get("duration_seconds")
        )

        db.session.add(workout_exercise)
        db.session.commit()

    except ValueError as error:
        db.session.rollback()
        return jsonify({"error": str(error)}), 400

    return jsonify({
        "id": workout_exercise.id,
        "workout_id": workout_exercise.workout_id,
        "exercise_id": workout_exercise.exercise_id,
        "reps": workout_exercise.reps,
        "sets": workout_exercise.sets,
        "duration_seconds": workout_exercise.duration_seconds
    }), 201


# --------------------------------------------------
# Start the application
# --------------------------------------------------
if __name__ == "__main__":
    app.run(port=5555, debug=True)