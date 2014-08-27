"""
Finds similar words using built-in english words list. Can be used to implement
"Did you mean [sth]".

Spell corrector based on: http://norvig.com/spell-correct.html
Word list taken from:
https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists#Project_Gutenberg
"""

import collections


def parse_words(lines):
    model = collections.defaultdict(lambda: 1)
    for line in lines:
        split = line.split(' ')
        model[split[0]] = int(split[1])
    return model


WORDS = parse_words(open('words-en.txt').read().split('\n'))

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'


def edits(word):
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]

    inserts = [a + c + b for a, b in splits for c in ALPHABET]
    deletes = [a + b[1:] for a, b in splits if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b) > 1]
    replaces = [a + c + b[1:] for a, b in splits for c in ALPHABET if b]

    return set(inserts + deletes + transposes + replaces)


def are_edits_correct(word):
    """
    Returns a set of correct edits (edits of edits to be more exact) of passed
    word.

    >>> are_edits_correct("collect")
    {'collector', 'collects', 'collect', 'recollect', 'connect', 'collected',
     'coldest', 'college', 'colleen', 'correct'}

    :param word: the word to check
    :return: set of correct edits of the word
    """
    return set(edit2 for edit in edits(word) for edit2 in edits(edit) if
               edit2 in WORDS)


def is_correct(words):
    """
    Returns the set with correct words passed in words list.
    :param words: list of words to check
    :return: set with the words that are correct
    """
    return set(word for word in words if word in WORDS)


def correct(word):
    """
    Corrects the word if it's not found in the built-in word list (and there's
    a word that's correct and similar enough).

    :param word: the word to correct
    :return: corrected word or passed word if it was correct (or no correct
             word was found)
    """
    word = word.lower()
    candidates = is_correct([word]) or is_correct(
        edits(word)) or are_edits_correct(word) or [word]
    return max(candidates, key=WORDS.get)


def correct_words(words):
    """
    Probably the only function useful from the outside. Requires the list of
    words and returns list of tuples that contains corrected words and whether
    they were corrected or not.

    >>> similar.correct_words(["the", "COLECTOR"])
    [('the', False), ('collector', True)]

    :param words: list of words
    :return: list of tuples that contains single word and whether it was
             corrected or not
    """
    res = []
    for word in words:
        corrected = correct(word)
        res.append((corrected, corrected != word))
    return res
