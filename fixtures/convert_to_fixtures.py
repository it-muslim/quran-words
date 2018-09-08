
'''convert surah.json to fixtures from
https://github.com/semarketir/quranjson/tree/master/source'''

import json

with open('surah.json', encoding='utf-8') as data_file:
    data = json.load(data_file)

fixture_data = [
    {
        "model": "surah.Surah",
        "fields": {
            "surah_name": element['title'],
            "surah_ayah_count": element['count']}
    }
    for element in data]

with open('surah_fixture.json', 'w') as fp:
    json.dump(fixture_data, fp)
