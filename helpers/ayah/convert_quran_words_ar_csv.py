'''convert quran_words_ar.csv to django fixtures file'''
import json
from os import path
import csv
from pprint import pprint
from collections import defaultdict


def structure_surah_dict(data):
    '''parse raw csv data and build structured dict'''
    surah_dict = {}
    for surah, ayah, position, word in data[1:]:

        if surah not in surah_dict:
            surah_dict[surah] = {}

        if ayah not in surah_dict[surah]:
            surah_dict[surah][ayah] = []

        if word not in surah_dict[surah][ayah]:
            surah_dict[surah][ayah].append(word)

    return surah_dict


def structure_ayah_json(surah_dict):
    '''form import ready ayah list json from structured dict'''
    list_of_ayahs = []
    for surah, surah_values in surah_dict.items():
        for ayah, ayah_values in surah_values.items():
            element = {
                "model": "quran.Ayah",
                "fields": {
                    "surah_id": surah,
                    "id": ayah,
                    "text": ayah_values
                }
            }
            list_of_ayahs.append(element.copy())
    return list_of_ayahs


def main():
    fixture_dir = path.abspath(
        path.join(path.dirname(__file__), '../../quran/fixtures'))
    fixture_filename = 'ayahs_list.json'
    fixture_file = path.join(fixture_dir, fixture_filename)

    data = list()

    with open('quran-words-ar.csv', encoding='utf-8') as data_file:
        fieldnames = ("surah", "ayah", "position", "text")
        reader = csv.DictReader(data_file, fieldnames)
        for row in reader:
            data.append([
                row.get("surah"),
                row.get("ayah"),
                row.get("position"),
                row.get("text")])

    surah_dict = structure_surah_dict(data)
    ayah_list = structure_ayah_json(surah_dict)

    with open(fixture_file, 'w', encoding="utf8") as fp:
        json.dump(ayah_list, fp, sort_keys=True, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    main()
