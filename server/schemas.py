from marshmallow import Schema, fields, validate


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)

    name = fields.Str(
        required=True,
        validate=validate.Length(min=1)
    )

    category = fields.Str(
        required=True,
        validate=validate.Length(min=1)
    )

    equipment_needed = fields.Bool(required=True)


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)

    workout_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(required=True)

    reps = fields.Int(
        allow_none=True,
        validate=validate.Range(min=0)
    )

    sets = fields.Int(
        allow_none=True,
        validate=validate.Range(min=0)
    )

    duration_seconds = fields.Int(
        allow_none=True,
        validate=validate.Range(min=0)
    )


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)

    date = fields.Date(required=True)

    duration_minutes = fields.Int(
        required=True,
        validate=validate.Range(min=1)
    )

    notes = fields.Str(allow_none=True)