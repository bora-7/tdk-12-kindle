import logging
import json
import os

import requests

logging.basicConfig(level=logging.INFO)

headers = {
    "User-Agent": "APIs-Google (+https://developers.google.com/webmasters/APIs-Google.html)"
}

TIMEOUT = 10


def logged(func):
    """Decorator that logs when a function starts and ends executing."""

    def log_it(*args, **kwards):
        logging.info("%s: start", func.__name__)
        result = func(*args, **kwards)
        logging.info("%s: end", func.__name__)
        return result

    return log_it


@logged
def get_list_of_all_words():
    """Scrapes the tdk website to save list containing every word to json file."""
    api_url = "https://sozluk.gov.tr/autocomplete.json"

    result = requests.get(api_url, headers=headers, timeout=TIMEOUT)
    os.makedirs(os.path.dirname("../dict/autocomplete.json"), exist_ok=True)

    with open("../dict/autocomplete.json", "w", encoding="utf-8") as f:
        f.write("[")
        total_length = len(result.json())
        for index, word in enumerate(result.json()):
            json.dump(word, f, ensure_ascii=False)
            if index != total_length - 1:
                f.write(",")
            f.write("\n")
        f.write("]")


@logged
def divide_list_of_all_words():
    """Split autocomplete.json to chunks of 5000 words."""
    with open("../dict/autocomplete.json", "r", encoding="utf-8") as f:
        words = json.load(f)

    os.makedirs(os.path.dirname("../dict/words_split/"), exist_ok=True)
    new_file_name_template = "autocomplete_chunk_"
    cur_words = []
    file_num = 0

    length_of_words = len(words)
    for i, word in enumerate(words):
        cur_words.append(word)
        if (i != 0 and i % 5000 == 0) or i == length_of_words - 1:
            new_file_name = new_file_name_template + str(file_num)
            file_num += 1
            filepath = "../dict/words_split/" + new_file_name + ".json"
            with open(filepath, "w", encoding="utf-8") as f:
                f.write("[")
                total_length = len(cur_words)
                for index, word in enumerate(cur_words):
                    json.dump(word, f, ensure_ascii=False)
                    if index != total_length - 1:
                        f.write(",")
                    f.write("\n")
                f.write("]")
                cur_words.clear()


if __name__ == "__main__":
    get_list_of_all_words()
    divide_list_of_all_words()
