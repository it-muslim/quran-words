import shutil
import tempfile
from django.db import connection
from django.core import exceptions
from django.core.files import File
from django.conf import settings
from django.test import TestCase, SimpleTestCase
from .models import Ayah, Reciter, Recitation
from .fields import SegmentsField


class SegmentsFieldTestCase(TestCase):
    '''Test for SegmentsField'''

    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()
        self._original_media_root = settings.MEDIA_ROOT
        settings.MEDIA_ROOT = self.test_dir
        # get the 93rd ayah from the surah Al-Baqara
        self.ayah_2_93 = Ayah.objects.get(pk=100)
        # create a temporary audio
        file = tempfile.NamedTemporaryFile(suffix='.mp3')
        self.audio_ayah = File(file, name=file.name)
        # create a reciter
        self.husari = Reciter.objects.create(
            name="Mahmud Kh. al-Husary")

    def tearDown(self):
        # Delete a temporary directory
        shutil.rmtree(self.test_dir)
        settings.MEDIA_ROOT = self._original_media_root

    def test_refresh_segments(self):
        recitation = Recitation.objects.create(
            ayah=self.ayah_2_93, segments=[(12, 15), (15, 19), (20, 26)],
            reciter=self.husari, audio=self.audio_ayah)
        recitation.refresh_from_db(fields=['segments'])
        self.assertIsInstance(recitation.segments, list)
        self.assertEqual(
            recitation.segments, [(12, 15), (15, 19), (20, 26)])

    def test_defer(self):
        recitation = Recitation.objects.create(
            ayah=self.ayah_2_93, segments=[(1, 2), (3, 4), (5, 6)],
            reciter=self.husari, audio=self.audio_ayah)
        self.assertIsInstance(recitation.segments, list)
        self.assertEqual(
            recitation.segments, [(1, 2), (3, 4), (5, 6)])
        recitation = Recitation.objects.get(pk=recitation.pk)
        self.assertIsInstance(recitation.segments, list)
        self.assertEqual(
            recitation.segments, [(1, 2), (3, 4), (5, 6)])

        recitation = Recitation.objects.defer("segments").get(pk=recitation.pk)
        self.assertIsInstance(recitation.segments, list)
        self.assertEqual(recitation.segments, [(1, 2), (3, 4), (5, 6)])
        # Refetch for save
        recitation = Recitation.objects.defer("segments").get(pk=recitation.pk)
        recitation.save()
        recitation = Recitation.objects.get(pk=recitation.pk)
        self.assertIsInstance(recitation.segments, list)
        self.assertEqual(recitation.segments, [(1, 2), (3, 4), (5, 6)])

    def test_recitation_with_empty_segments(self):
        recitation = Recitation.objects.create(
            ayah=self.ayah_2_93, segments=[],
            reciter=self.husari, audio=self.audio_ayah)
        recitation.save()
        recitation = Recitation.objects.get(pk=recitation.pk)
        self.assertIsInstance(recitation.segments, list)
        self.assertEqual(recitation.segments, [])

    def test_recitation_with_empty_string_segments(self):
        recitation = Recitation.objects.create(
            ayah=self.ayah_2_93, segments="",
            reciter=self.husari, audio=self.audio_ayah)
        recitation.save()
        recitation = Recitation.objects.get(pk=recitation.pk)
        self.assertIsInstance(recitation.segments, list)
        self.assertEqual(recitation.segments, [])

    def test_recitation_with_wrong_length_segments_more_than_two(self):
        try:
            Recitation.objects.create(
                ayah=self.ayah_2_93, segments=[(12, 15), (15, 90, 100)],
                reciter=self.husari, audio=self.audio_ayah)
        except exceptions.ValidationError as e:
            self.assertEqual(
                str(e), "['Length of tuples must be equals 2']")

    def test_recitation_with_wrong_length_segments_less_than_two(self):
        with self.assertRaises(exceptions.ValidationError) as e:
            Recitation.objects.create(
                ayah=self.ayah_2_93, segments=[(12, 15), ()],
                reciter=self.husari, audio=self.audio_ayah)
        self.assertEqual(
            "['Length of tuples must be equals 2']", str(e.exception))

    def test_wrong_segments_not_containing_tuples(self):
        with self.assertRaises(exceptions.ValidationError) as e:
            Recitation.objects.create(
                ayah=self.ayah_2_93, segments=[12, 15, [15, 90, 100], None],
                reciter=self.husari, audio=self.audio_ayah)
        self.assertEqual(
            "['List must contains tuples only']", str(e.exception))

    def test_wrong_segments_with_no_list(self):
        with self.assertRaises(exceptions.ValidationError) as e:
            Recitation.objects.create(
                ayah=self.ayah_2_93, segments=(3, 5, 6),
                reciter=self.husari, audio=self.audio_ayah)
        self.assertEqual("['Segments must be a list']", str(e.exception))

    def test_segments_get_prep_value(self):
        field = SegmentsField()
        self.assertEqual(field.get_prep_value([(3, 4), (5, 7)]), "3:4,5:7")

    def test_segments_get_prep_value_with_empty_list(self):
        field = SegmentsField()
        self.assertEqual(field.get_prep_value([]), "")

    def test_segments_get_prep_value_with_None(self):
        field = SegmentsField()
        self.assertEqual(field.get_prep_value(None), None)

    def test_segments_get_prep_value_with_empty_string(self):
        field = SegmentsField()
        self.assertEqual(field.get_prep_value(""), "")

    def test_segments_get_prep_value_with_no_list(self):
        field = SegmentsField()
        with self.assertRaises(exceptions.ValidationError) as e:
            field.get_prep_value({3, 4, (5, 7)})
        self.assertEqual(
            "['Segments must be a list']", str(e.exception))

    def test_segments_get_prep_value_with_list_not_containing_tuples(self):
        field = SegmentsField()
        with self.assertRaises(exceptions.ValidationError) as e:
            field.get_prep_value([3, 4, [5, 7]])
        self.assertEqual(
            "['List must contains tuples only']", str(e.exception))

    def test_segments_get_prep_value_with_length_of_tuples_less_than_two(self):
        field = SegmentsField()
        with self.assertRaises(exceptions.ValidationError) as e:
            field.get_prep_value([(3,), (5, 7)])
        self.assertEqual(
            "['Length of tuples must be equals 2']", str(e.exception))

    def test_segments_get_prep_value_with_length_of_tuples_more_than_two(self):
        field = SegmentsField()
        with self.assertRaises(exceptions.ValidationError) as e:
            field.get_prep_value([(3, 5), (5, 7, 9, 10)])
        self.assertEqual(
            "['Length of tuples must be equals 2']", str(e.exception))

    def test_segments_to_python_method(self):
        field = SegmentsField()
        self.assertEqual(field.to_python("3:4,5:7"), [(3, 4), (5, 7)])

    def test_segments_to_python_method_with_list(self):
        field = SegmentsField()
        self.assertEqual(field.to_python([(3, 4), (5, 7)]), [(3, 4), (5, 7)])

    def test_segments_to_python_method_with_empty_string(self):
        field = SegmentsField()
        self.assertEqual(field.to_python(""), [])

    def test_segments_to_python_method_with_None(self):
        field = SegmentsField()
        self.assertEqual(field.to_python(None), None)

    def test_segments_to_python_method_with_wrong_segments_one_segment(self):
        field = SegmentsField()
        with self.assertRaises(exceptions.ValidationError) as e:
            field.to_python("3,5:7")
        self.assertEqual("['Invalid string of segments']", str(e.exception))

    def test_segments_to_python_method_with_wrong_segments_four_segments(self):
        field = SegmentsField()
        with self.assertRaises(exceptions.ValidationError) as e:
            field.to_python("3:20:30:50,5:7")
        self.assertEqual("['Invalid string of segments']", str(e.exception))


class SegmentsFieldDeconstructionTests(SimpleTestCase):
    """Tests the deconstruct() method on SegmentsField."""

    def test_name(self):
        """
        Tests the outputting of the correct name if assigned one.
        """
        field = SegmentsField()
        name, path, args, kwargs = field.deconstruct()
        self.assertIsNone(name)
        field.set_attributes_from_name("segments")
        name, path, args, kwargs = field.deconstruct()
        self.assertEqual(name, "segments")

    def test_segments_field(self):
        field = SegmentsField()
        name, path, args, kwargs = field.deconstruct()
        self.assertEqual(path, "quran.fields.SegmentsField")
        self.assertEqual(args, [])
        self.assertEqual(kwargs, {})
        field = SegmentsField(null=True, blank=True)
        name, path, args, kwargs = field.deconstruct()
        self.assertEqual(path, "quran.fields.SegmentsField")
        self.assertEqual(args, [])
        self.assertEqual(kwargs, {"null": True, "blank": True})

    def test_db_parameters_respects_db_type(self):
        f = SegmentsField()
        self.assertEqual(f.db_parameters(connection)['type'], 'text')
