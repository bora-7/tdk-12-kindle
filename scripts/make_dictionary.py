import logging
import json
import sys
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


def get_word_meaning(word):
    """
    Retrieves the meaning of a specific word from the TDK website.
    """
    try:
        api_url = "https://sozluk.gov.tr/gts?ara=" + word
        result = requests.get(api_url, headers=headers, timeout=TIMEOUT)
        result.raise_for_status()
        return result.json()
    except requests.exceptions.RequestException as e:
        logging.error("Error occurred for word '%s': %s", word, e)
        with open("../dict/error-words.txt", "a", encoding="utf-8") as f:
            f.write(word)
            f.write("\n")


def remove_html_properties(word_meaning):
    """Some properties of the word are unwanted, they are specified and removed."""
    top_level_properties = ["madde_html", "on_taki_html", "telaffuz_html", "lisan_html"]
    for prop in top_level_properties:
        if prop in word_meaning:
            del word_meaning[prop]

    sub_level_properties = [("anlamlarListe", "anlam_html")]
    for top_key, sub_key in sub_level_properties:
        if top_key not in word_meaning:
            return {"error": "word doesn't exist."}
        for prop in word_meaning[top_key]:
            if sub_key in prop:
                del prop[sub_key]

    return word_meaning


def process_word(word):
    """Function that gets the definition and filters, used for concurrency."""
    # temporary fix for 1 and 18
    word_meaning = get_word_meaning(word["madde"])
    if not word_meaning or "error" in word_meaning:
        return {"skipped-word": word["madde"]}
    # print(word_meaning)
    if len(word_meaning) == 1:
        word_meaning_filtered = remove_html_properties(word_meaning[0])
    else:
        word_meaning_filtered = remove_html_properties(word_meaning[-1])

    if "error" in word_meaning_filtered:
        return {"skipped-word": word["madde"]}
    return word_meaning_filtered


@logged
def make_dictionary_json(chunk_number, checkpoint_word=None):
    """Use the list of words to concurrently make a dictionary."""
    chunk_path = "../dict/words_split/autocomplete_chunk_" + str(chunk_number) + ".json"
    with open(chunk_path, "r", encoding="utf-8") as f:
        words = json.load(f)

    checkpoint = 0

    if checkpoint_word:
        checkpoint = words.index({"madde": checkpoint_word}) + 1
    print(f"checkpoint:  {checkpoint}")
    index = checkpoint
    total_word_count = len(words)
    skipped_word_count = 0

    os.makedirs(os.path.dirname("../dict/results_split/"), exist_ok=True)
    os.makedirs(os.path.dirname("../dict/not_found_words_split/"), exist_ok=True)
    result_path = "../dict/results_split/split_" + str(chunk_number) + ".json"
    not_found_words_path = (
        "../dict/not_found_words_split/split_" + str(chunk_number) + ".txt"
    )

    with open(result_path, "w", encoding="utf-8") as f2, open(
        not_found_words_path, "w", encoding="utf-8"
    ) as f3:
        f2.write("[")
        for word in words:
            result = process_word(word)

            print(f"{index}/{total_word_count}")
            if "skipped-word" not in result:
                json.dump(result, f2, ensure_ascii=False)
                if index != total_word_count - 1:
                    f2.write(",")
                f2.write("\n")
            else:
                skipped_word_count += 1
                f3.write(result["skipped-word"])
                f3.write("\n")
            index += 1
        f2.write("]")

    print("number of skipped words: " + str(skipped_word_count))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Don't forget to supply chunk number")
        sys.exit()
    elif not os.path.isdir("../dict"):
        print("You need to run get-all-words.py first!")
        sys.exit()

    chunk_number = sys.argv[1]

    # Take in a chunk number, and write the results for it.
    make_dictionary_json(chunk_number)
