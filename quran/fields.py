from django.core.exceptions import ValidationError
from django.db import models


class SegmentsField(models.TextField):
    description = "Segments"

    def to_python(self, value):
        if value is None:
            return None
        # if value is empty string return empty list
        if value == '':
            return []
        # if value is list
        if isinstance(value, list):
            # if list is not empty
            if value:
                # validate list of tuples
                self._validate_tuples_containing_in_list(value)
                self._validate_length_of_segments(
                    value, "Length of tuples must be equals 2")
            return value
        try:
            # try to parse a string of segments from DB to a list of tuples
            # "12:15,16:19" => [(12, 15), (16, 19)]
            segments_list = [tuple(
                int(timecode) for timecode in timecodes.split(':'))
                for timecodes in value.split(',')]
            # validate list of tuples
            self._validate_length_of_segments(
                segments_list, 'Invalid string of segments')
            return segments_list

        except (TypeError, ValueError, IndexError):
            raise ValidationError(
                message='Invalid string of segments',
                code='invalid')

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def get_prep_value(self, value):
        # save to DB None or empty string
        if value is None or value == '':
            return value
        # if value is not a list
        if not isinstance(value, list):
            raise ValidationError(
                message="Segments must be a list", code="invalid")
        # if list is empty return empty string
        if not value:
            return ''

        # validate list of tuples
        self._validate_tuples_containing_in_list(value)
        self._validate_length_of_segments(
            value, "Length of tuples must be equals 2")
        # return formatted string of segments
        # [(12, 15), (16, 19)] => "12:15,16:19"
        return ','.join(
            (f'{segment_pair[0]}:{segment_pair[1]}'
                for segment_pair in value))

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_prep_value(value)

    def _validate_tuples_containing_in_list(self, value):
        for segments in value:
            # if no tuples in value
            if type(segments) != tuple:
                raise ValidationError(
                    message='List must contains tuples only',
                    code='invalid')

    def _validate_length_of_segments(self, value, message):
        '''Check if length of tuples in a list equal two'''
        for segments in value:
            if len(segments) != 2:
                raise ValidationError(
                    message=message,
                    code="invalid")
