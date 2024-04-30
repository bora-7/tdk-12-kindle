import logging
import json


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
def append_results():
    """
    Iterate over the results for the 20 chunks created by
    earlier functions, and aggregate all results to the same file.
    """
    result_path = "../dict/tdk-12.json"

    with open(result_path, "w", encoding="utf-8") as f2:
        f2.write("[")

        for i in range(20):
            split_path = "../dict/results_split/split_" + str(i) + ".json"

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
    result_path = "../dict/all_not_found_words.txt"

    with open(result_path, "w", encoding="utf-8") as f2:
        for i in range(20):
            split_path = "../dict/not_found_words_split/split_" + str(i) + ".txt"

            with open(split_path, "r", encoding="utf-8") as f_split:
                for line in f_split:
                    f2.write(line)


def find_word_in_tdk11(word):
    tdk11_path = "../dict/tdk11.json"
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
    append_results()
    append_not_found_words()
    try_words_again()
