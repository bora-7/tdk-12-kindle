import logging
import json
import concurrent.futures
from tenacity import retry, stop_after_attempt, wait_exponential
import time

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
        f.write('[')
        total_length = len(result.json())
        for index, word in enumerate(result.json()):
            json.dump(word, f, ensure_ascii=False)
            if index != total_length-1:
                f.write(',')
            f.write('\n')
        f.write(']')

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
        if (i != 0 and i % 5000 == 0) or i == length_of_words-1:
            new_file_name = new_file_name_template + str(file_num)
            file_num += 1
            filepath = "../dict/words_split/" + new_file_name + ".json"
            with open(filepath, "w", encoding="utf-8") as f:
                f.write('[')
                total_length = len(cur_words)
                for index, word in enumerate(cur_words):
                    json.dump(word, f, ensure_ascii=False)
                    if index != total_length-1:
                        f.write(',')
                    f.write('\n')
                f.write(']')
                cur_words.clear()

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=60))
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
        for prop in word_meaning[top_key]:
            if sub_key in prop:
                del prop[sub_key]

    return word_meaning


def process_word(word):
    """Function that gets the definition and filters, used for concurrency."""
    word_meaning = get_word_meaning(word["madde"])
    if not word_meaning or "error" in word_meaning:
        return {"skipped-word": word["madde"]}
    print(word_meaning)
    word_meaning_filtered = remove_html_properties(word_meaning[0])
    return word_meaning_filtered

@logged
def make_dictionary_json(chunk_number, checkpoint_word=None, checkpoint_index = None):
    """Use the list of words to concurrently make a dictionary."""
    chunk_path = "../dict/words_split/autocomplete_chunk_" + str(chunk_number) + ".json"
    with open(chunk_path, "r", encoding="utf-8") as f:
        words = json.load(f)

    checkpoint = 0

    if checkpoint_word:
        checkpoint = words.index({"madde": checkpoint_word}) + 1
    elif checkpoint_index:
        checkpoint = checkpoint_index
    print(f"checkpoint:  {checkpoint}")
    index = checkpoint
    total_word_count = len(words)
    skipped_word_count = 0

    result_path = "../dict/results_split/split_" + str(chunk_number) + ".json"
    not_found_words_path = "../dict/not_found_words_split/split_" + str(chunk_number) + ".txt"

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executer, open(
        result_path, "w", encoding="utf-8"
    ) as f2, open(not_found_words_path, "w", encoding="utf-8") as f3:
        f2.write("[")
        futures = [executer.submit(process_word, word) for word in words[checkpoint:]]
        for future in concurrent.futures.as_completed(futures):
            if index % 100 == 0:
                print(f"{index}/{total_word_count}")
            result = future.result()
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


# SEQUENTIAL:
# It took 67 seconds for 100 entries.
# 66489.46 seconds expected for all entries.
# 1108 minutes
# 18.46 hours

# CONCURRENT
# Takes around 5 seconds for 100 entries.
# Should take 82 minutes in total.

# CHECKPOINTS:
# bağlaçlı tamlama
# bağlaçlı
    

# IFFY AREAS:
# 8300
# 

if __name__ == "__main__":
    # get_list_of_all_words()
    # divide_list_of_all_words()


    # Take in a chunk number, and write the results for it.
    make_dictionary_json(1)
