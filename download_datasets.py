import os
import bz2
import requests
import shutil
import mwparserfromhell
from pathlib import Path
from xml.etree.ElementTree import iterparse

def download_file(url, output_file):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(output_file, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

def download_wikipedia():
    wikipedia_dump_url = 'https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2'
    output_file = 'datasets/wikipedia_dump.xml.bz2'
    download_file(wikipedia_dump_url, output_file)
    parse_wikipedia_dump(output_file, 'datasets/wikipedia_text.txt')

def parse_wikipedia_dump(input_file, output_file):
    with bz2.open(input_file, 'rt', encoding='utf-8') as f:
        context = iterparse(f, events=('start', 'end'))
        context = iter(context)
        with open(output_file, 'w', encoding='utf-8') as out_file:
            for event, elem in context:
                if event == 'end' and elem.tag.endswith('text'):
                    wikicode = mwparserfromhell.parse(elem.text)
                    plain_text = wikicode.strip_code(normalize=True)
                    out_file.write(plain_text + '\n\n')
                elem.clear()

def download_gutenberg_books():
    gutenberg_books = [
        '1342',  # Pride and Prejudice
        '84',    # Frankenstein
        '11',    # Alice's Adventures in Wonderland
        '1661',  # The Adventures of Sherlock Holmes
        '2701',  # Moby Dick
    ]
    gutenberg_base_url = 'https://www.gutenberg.org/files'

    for book_id in gutenberg_books:
        url = f'{gutenberg_base_url}/{book_id}/{book_id}.txt'
        output_file = f'datasets/gutenberg_book_{book_id}.txt'
        download_file(url, output_file)

def main():
    if not os.path.exists('datasets'):
        os.makedirs('datasets')

    download_wikipedia()
    download_gutenberg_books()

if __name__ == '__main__':
    main()
