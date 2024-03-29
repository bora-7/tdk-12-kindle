## TDK-12
This project contains the 12th edition of 'Guncel Turkce Sozluk' (translated to 'up-to-date Turkish dictionary'). This project is inspired by @ogun's [guncel-turkce-sozluk](https://github.com/ogun/guncel-turkce-sozluk) project.

This dictionary contains 99,182 definitions. This is 6776 definitions more than the 11th edition. Many definitions have been updated.

The json file that contains all the definitions is inside the `tdk-12` folder. This file is zipped and is 11.8 MB in size. After it's decompressed, it's 124.8 MB.

## Kindle
The Kindle and Kobo port of this dictionary is being made. The link will be put here when it's done.

## Code
For those who are interested, the code can be found inside the `src` directory.

The code is split into 3 Python scripts:
- `get_all_words.py`: This script saves all words into the `autocomplete.json` file. Because the dictionary is very large, this file is then split into 20 different chunks. This will make the later steps easier and allow for concurrency while scraping.
- `make_dictionary.py`: Takes in a chunk number, and puts the definitions for the words in that chunk into another file. The words whose definition are not found are written into a different file.
- `combine_results.py`: When the results for each chunk are written, this script will append all the results into the same JSON file. The words that were previously skipped are tried again, and if required, their definition is taken from tdk-11.
