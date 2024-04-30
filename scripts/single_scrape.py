import logging
import json
import sys

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


@logged
def append_results():
    """
    Iterate over the results for the 20 chunks created by
    earlier functions, and aggregate all results to the same file.
    """
    result_path = "../dict-full/tdk-12.json"

    with open(result_path, "w", encoding="utf-8") as f2:
        f2.write("[")

        for i in range(20):
            split_path = "../dict-full/results_split/split_" + str(i) + ".json"

            with open(split_path, "r", encoding="utf-8") as f3:
                results = json.load(f3)

                for index, result in enumerate(results):
                    json.dump(result, f2, ensure_ascii=False)
                    if i != 19 or index != len(results) - 1:
                        f2.write(",")
                    f2.write("\n")

        f2.write("]")


@logged
def append_not_found_words():
    """
    Iterate over the not found words for 20 chunks, put them in the same text file.
    """
    result_path = "../dict-full/all_not_found_words.txt"

    with open(result_path, "w", encoding="utf-8") as f2:
        for i in range(20):
            split_path = "../dict-full/not_found_words_split/split_" + str(i) + ".txt"

            with open(split_path, "r", encoding="utf-8") as f_split:
                for line in f_split:
                    f2.write(line)


def find_word_in_tdk11(word):
    tdk11_path = "../dict-full/tdk11.json"
    with open(tdk11_path, "r", encoding="utf-8") as tdk11:
        for line in tdk11:
            item = json.loads(line.strip())
            if "madde" in item and item["madde"] == word:
                del item["_id"]
                return item
    
    return {"skipped-word": word}


@logged
def try_words_again():
    """
    Iterate through all the not found words and see if they work.
    """
    skipped_word_count = 0

    result_path = "../dict-full/retried_words.json"
    new_not_found_words_path = "../dict-full/retried-failed.txt"

    all_not_found_words_path = "../dict-full/all_not_found_words.txt"
    with open(result_path, "w", encoding="utf-8") as f2, open(
        new_not_found_words_path, "w", encoding="utf-8"
    ) as f3:
        f2.write("[")
        with open(all_not_found_words_path, "r", encoding="utf-8") as f4:
            count = 0
            for line in f4:
                word = line.strip().lower()
                word_dict = {"madde": word}
                # result = process_word(word_dict)
                result = find_word_in_tdk11(word)
                print(f"line number: {count}")
                if "skipped-word" not in result:
                    json.dump(result, f2, ensure_ascii=False)
                    f2.write(",")
                    f2.write("\n")
                else:
                    skipped_word_count += 1
                    f3.write(result["skipped-word"])
                    f3.write("\n")
                count += 1
        f2.write("]")

    print(f"skipped words count: {skipped_word_count}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("don't forget to supply chunk number")
        sys.exit()

    chunk_number = sys.argv[1]
    # get_list_of_all_words()
    # divide_list_of_all_words()

    # Take in a chunk number, and write the results for it.
    # make_dictionary_json(chunk_number)
    # append_results()
    # append_not_found_words()
    try_words_again()
