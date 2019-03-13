"""
Some basic admin tests.
Tests the various admin callbacks.
"""
from django.test import TestCase
from recite.admin import ReciterAdmin


class ReciteAdminTest(TestCase):
    """
    Admin panel tests.
    Reciter and Recitations managing functions unit testing.
    """
    def test_get_file_paths_dict(self):
        """
        Test that function returns only valid surah ayah strucured dict
        ignoring malformed filenames
        :param csv_content_sorted: a list of OrderedDicts from parsed csv file
        csv_content_sorted = [
            OrderedDict(
                [
                    ('sura', '1'),
                    ('ayat', '1'),
                    ('segments', '[[0, 1, 60, 610], [1, 2, 620, 1310]]')
                ]
            ),
            OrderedDict(
                [
                    ('sura', '1'),
                    ('ayat', '2'),
                    ('segments', '[[0, 1, 80, 960], [1, 2, 970, 1800]]')
                ]
            )
        ]
        :return: file_paths[surah_number][ayah_number] = filepath
        :rtype: defaultdict
        """
        pass
