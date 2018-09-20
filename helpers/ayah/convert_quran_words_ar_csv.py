'''Convert quran_words_ar.csv to django fixtures file'''
import json
from os import path
import csv
from collections import defaultdict


def structure_surah_dict(data):
    '''Parse raw csv data and build structured dict'''
    surah_dict = defaultdict(lambda: defaultdict(list))
    for surah, ayah, position, word in data:
        surah_dict[surah][ayah].append(word)
    return surah_dict


def structure_ayah_json(surah_dict):
    '''Form import ready ayah list json from structured dict'''
    list_of_ayahs = []
    for surah, ayahs in surah_dict.items():
        for ayah, words in ayahs.items():
            element = {
                "model": "quran.Ayah",
                "fields": {
                    "surah": surah,
                    "ayah": ayah,
                    "text": words
                }
            }
            list_of_ayahs.append(element)
    return list_of_ayahs


def main():
    fixture_dir = path.abspath(
        path.join(path.dirname(__file__), '../../quran/fixtures'))
    fixture_filename = 'ayah_list.json'
    fixture_file = path.join(fixture_dir, fixture_filename)

    data = list()

    with open('quran-words-ar.csv', encoding='utf-8') as data_file:
        fieldnames = ("surah", "ayah", "position", "text")
        reader = csv.DictReader(data_file, fieldnames)
        for row in reader:
            data.append([
                int(row.get("surah")),
                int(row.get("ayah")),
                int(row.get("position")),
                row.get("text")])

    surah_dict = structure_surah_dict(data)
    ayah_list = structure_ayah_json(surah_dict)

    with open(fixture_file, 'w', encoding="utf8") as fp:
        json.dump(ayah_list, fp, sort_keys=True, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    main()
