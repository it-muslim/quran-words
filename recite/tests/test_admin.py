"""
Admin tests.

Tests the various admin callbacks.
"""
from unittest import mock
from django.test import TestCase
from recite.admin import ReciterAdmin


class ReciteAdminTest(TestCase):
    """
    Admin panel tests.

    Reciter and Recitations admin management functions unit testing.
    """

    def test_get_file_paths_dict(self):
        """
        Test that function returns only valid surah ayah strucured dict.

        Parse mocked directory and return structured dict of filenames,
        `file_paths[surah_number][ayah_number] = filepath`
        Ignore malformed filenames.
        """
        with mock.patch('os.walk') as mock_walk:
            # mocked os.walk returns fake directory
            mock_walk.return_value = [
                ('\\tmp', ['Al-Test'], []),
                ('\\tmp\\Al-Test', [], [
                    'index.html',
                    '000_checksum.md5',
                    '001001.mp3',   # valid filename format
                    '001002.mp3',   # valid filename format
                    '002001.mp3',   # valid filename format
                    'bismillah.mp3']),
            ]
            file_paths = ReciterAdmin.get_file_paths_dict("directory")

        expected_dict = {
            1: {
                1: '\\tmp\\Al-Test\\001001.mp3',
                2: '\\tmp\\Al-Test\\001002.mp3'
            },
            2: {1: '\\tmp\\Al-Test\\002001.mp3'},
        }

        self.assertDictEqual(file_paths, expected_dict)
