from datetime import date

from app import app
from models import db, Exercise, Workout, WorkoutExercise


with app.app_context():
    # Clear existing data
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    # Create exercises
    push_up = Exercise(
        name="Push-up",
        category="Strength",
        equipment_needed=False
    )

    squat = Exercise(
        name="Squat",
        category="Strength",
        equipment_needed=False
    )

    treadmill = Exercise(
        name="Treadmill Running",
        category="Cardio",
        equipment_needed=True
    )

    # Add exercises
    db.session.add_all([
        push_up,
        squat,
        treadmill
    ])

    db.session.commit()

    # Create workout
    workout = Workout(
        date=date.today(),
        duration_minutes=45,
        notes="Full body workout"
    )

    db.session.add(workout)
    db.session.commit()

    # Add exercises to the workout
    workout_pushups = WorkoutExercise(
        workout_id=workout.id,
        exercise_id=push_up.id,
        reps=15,
        sets=3
    )

    workout_squats = WorkoutExercise(
        workout_id=workout.id,
        exercise_id=squat.id,
        reps=20,
        sets=3
    )

    workout_running = WorkoutExercise(
        workout_id=workout.id,
        exercise_id=treadmill.id,
        duration_seconds=600
    )

    db.session.add_all([
        workout_pushups,
        workout_squats,
        workout_running
    ])

    db.session.commit()

    print("Database seeded successfully!")