from django.db import connection
from django.core.exceptions import ValidationError
from django.test import TestCase, SimpleTestCase
from recite.fields import SegmentsField


class SegmentsFieldTestCase(TestCase):
    """Test for SegmentsField"""

    def setUp(self):
        self.field = SegmentsField()

    def test_segmentsfield_cleans_valid_string(self):
        self.assertEqual(self.field.clean("3:4,5:7", None), [(3, 4), (5, 7)])

    def test_segmentsfield_raises_error_on_invalid_intput(self):
        with self.assertRaises(ValidationError):
            self.field.clean("a", None)

    def test_segmentsfield_raises_error_on_empty_string(self):
        with self.assertRaises(ValidationError):
            self.field.clean("", None)

    def test_segmentsfield_cleans_empty_string_when_blank_true(self):
        f = SegmentsField(blank=True)
        self.assertEqual([], f.clean("", None))

    def test_segmentsfield_raises_error_on_empty_input(self):
        f = SegmentsField(null=False)
        with self.assertRaises(ValidationError):
            f.clean(None, None)
        with self.assertRaises(ValidationError):
            f.clean("", None)

    def test_default(self):
        f = SegmentsField(default=[(12, 89), (100, 180)])
        self.assertEqual(f.get_default(), [(12, 89), (100, 180)])

    def test_segmentsfield_get_prep_value(self):
        self.assertEqual(
            self.field.get_prep_value([(3, 4), (5, 7)]), "3:4,5:7"
        )
        self.assertIsNone(self.field.get_prep_value(None))
        self.assertEqual(self.field.get_prep_value([(3, 4)]), "3:4")
        self.assertEqual(self.field.get_prep_value("3:9,10:12"), "3:9,10:12")
        self.assertEqual(self.field.get_prep_value([]), "")
        self.assertEqual(self.field.get_prep_value(""), "")
        # wrong segments: not a list
        expected_message = (
            "['Unable to decode anything other than list and string']"
        )
        with self.assertRaisesMessage(ValidationError, expected_message):
            self.field.get_prep_value({3, 4, (5, 7)})
        # wrong segments: list without tuples
        expected_message = "['List must contain tuples only']"
        with self.assertRaisesMessage(ValidationError, expected_message):
            self.field.get_prep_value([3, 4, [5, 7]])
        # wrong segments: length of tuples less than two
        expected_message = "['Length of tuples must be equals 2']"
        with self.assertRaisesMessage(ValidationError, expected_message):
            self.field.get_prep_value([(3,), (5, 7)])
        # wrong segments: length of tuples more than two
        with self.assertRaisesMessage(ValidationError, expected_message):
            self.field.get_prep_value([(3, 5), (5, 7, 9, 10)])

    def test_segmentsfield_to_python(self):
        self.assertIsNone(self.field.to_python(None))
        self.assertEqual(self.field.to_python(""), [])
        self.assertEqual(self.field.to_python("3:4,5:7"), [(3, 4), (5, 7)])
        self.assertEqual(
            self.field.to_python([(3, 4), (5, 7)]), [(3, 4), (5, 7)]
        )
        # wrong segments
        expected_message = "['Length of tuples must be equals 2']"
        with self.assertRaisesMessage(ValidationError, expected_message):
            self.field.to_python("3,5:7")
        with self.assertRaisesMessage(ValidationError, expected_message):
            self.field.to_python("3:20:30:50,5:7")
        expected_message = "['Invalid string of segments']"
        with self.assertRaisesMessage(ValidationError, expected_message):
            self.field.to_python("a:b,c:d")


class SegmentsFieldDeconstructionTests(SimpleTestCase):
    """Tests the deconstruct() method on SegmentsField."""

    def setUp(self):
        self.field = SegmentsField()

    def test_name(self):
        """
        Tests the outputting of the correct name if assigned one.
        """
        name, path, args, kwargs = self.field.deconstruct()
        self.assertIsNone(name)
        self.field.set_attributes_from_name("segments")
        name, path, args, kwargs = self.field.deconstruct()
        self.assertEqual(name, "segments")

    def test_segmentsfield(self):
        name, path, args, kwargs = self.field.deconstruct()
        self.assertEqual(path, "recite.fields.SegmentsField")
        self.assertEqual(args, [])
        self.assertEqual(kwargs, {})
        self.field = SegmentsField(null=True, blank=True)
        name, path, args, kwargs = self.field.deconstruct()
        self.assertEqual(path, "recite.fields.SegmentsField")
        self.assertEqual(args, [])
        self.assertEqual(kwargs, {"null": True, "blank": True})

    def test_db_parameters_respects_db_type(self):
        self.assertEqual(self.field.db_parameters(connection)["type"], "text")
