from django.core import exceptions
from django.db import models


class SegmentsField(models.TextField):
    description = "A custom field to save list of timecodes in DB as a string"

    def to_python(self, segments):
        if isinstance(segments, list) or segments is None or segments == '':
            return segments
        try:
            return [
                tuple(int(timecode) for timecode in timecodes.split(':'))
                for timecodes in segments.split(',')]
        except (TypeError, ValueError):
            raise exceptions.ValidationError(
                message='Invalid string of segments',
                code='invalid',
            )

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def get_prep_value(self, segments_list):
        if segments_list is None or segments_list == '':
            return segments_list

        if not isinstance(segments_list, list):
            raise exceptions.ValidationError(
                message="Segments must be a list", code="invalid")

        for segments in segments_list:
            if len(segments) != 2:
                raise exceptions.ValidationError(
                    message="Length of tuple must be equals 2",
                    code="invalid")

        return ','.join(
            (f'{segment_pair[0]}:{segment_pair[1]}'
                for segment_pair in segments_list))

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_prep_value(value)
