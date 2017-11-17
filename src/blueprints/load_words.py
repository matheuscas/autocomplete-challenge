import json
import os, sys

current_directory = os.getcwd()

def load_words():
    file_path = current_directory + '/blueprints/words.txt'
    words = []
    with open(file_path) as words_file:
        for word in words_file.readlines():
            if len(word) >= 2:
                words.append(word.strip())
    return words
