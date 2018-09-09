'''convert surah.json from quranjson project
https://github.com/semarketir/quranjson/blob/master/source/surah.json
to django fixtures file'''

import json
from os import path

fixture_dir = path.abspath(
    path.join(path.dirname(__file__), '../../quran/fixtures'))
fixture_filename = 'surah_data_init.json'
fixture_file = path.join(fixture_dir, fixture_filename)

with open('surah.json', encoding='utf-8') as data_file:
    data = json.load(data_file)

surah_data = [
    {
        "model": "quran.Surah",
        "fields": {
            "surah_name": element['title'],
            "surah_ayah_count": element['count']}
    }
    for element in data]

with open(fixture_file, 'w') as fp:
    json.dump(surah_data, fp, sort_keys=True, indent=4)
