from django.core.exceptions import ValidationError
from django.db import models


class SegmentsField(models.TextField):
    description = "Segments"

    def to_python(self, value):
        if value is None:
            return None
        if not value:
            return []
        if not isinstance(value, list) and not isinstance(value, str):
            raise ValidationError(
                message="Unable to decode anything other than list and string",
                code="invalid",
            )
        if isinstance(value, str):
            try:
                # try to convert a string of segments to a list of tuples
                # "12:15,16:19" => [(12, 15), (16, 19)]
                value = [
                    tuple(int(segment) for segment in segments.split(":"))
                    for segments in value.split(",")
                ]

            except (TypeError, ValueError, IndexError):
                raise ValidationError(
                    message="Invalid string of segments", code="invalid"
                )
        self._validate_tuples(value)
        self._validate_lengths(value)
        return value

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        if value is None:
            return value
        # return formatted string of segments
        # [(12, 15), (16, 19)] => "12:15,16:19"
        return ",".join((f"{segment[0]}:{segment[1]}" for segment in value))

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_prep_value(value) if value else ""

    def _validate_tuples(self, value):
        """Check if only tuples contain in the list"""
        all_tuples = all(isinstance(segment, tuple) for segment in value)
        if not all_tuples:
            raise ValidationError(
                message="List must contain tuples only", code="invalid"
            )

    def _validate_lengths(self, value):
        """Check if all tuple lengths equal two."""
        all_equal_two = all((len(segment) == 2 for segment in value))
        if not all_equal_two:
            raise ValidationError(
                message="Length of tuples must be equals 2", code="invalid"
            )
