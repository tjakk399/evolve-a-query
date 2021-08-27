from __future__ import annotations

from typing import Dict, List, Optional, Set

from collections import defaultdict

import random


class Vocabulary():
    """Class for managing vocabulary.

    :param words: List of words from some text,
        defaults to [].
    :type words: List[str], optional
    """

    def __init__(self, words: List(str) = []):
        """Constructor method
        """
        self.words = defaultdict(int)
        self.add_words(words)

    def __str__(self):
        return "\n".join(
                [
                    "{:>5} {}".format(count, word)
                    for word, count in sorted(
                        self.words.items(),
                        key = lambda item: item[1],
                        reverse = True
                        )
                    ]
                )

    @staticmethod
    def _tokenized(text: str) -> List[str]:
        """Returns tokenized string.

        :param text: String
        :type text: str

        :return: List of words
        :rtype: List[str]
        """
        return text.split()

    def add_words(self, words: List[str]) -> None:
        """Adds word to dictionary counter.

        :param words: List of words
        :type words: List[str]
        """
        for word in words:
            self.words[word] += 1

    def add_words_from(self, text: str) -> None:
        """Adds words from text to dictionary counter.

        :param text: Text string
        :type text: str
        """
        self.add_words(
                Vocabulary._tokenized(text)
                )

    def sample(self,
            n: int = 1,
            without: List[str] = []
            ) -> List[str]:
        """Returns random sample words from vocabulary.

        :param n: Number of sample words to be returned
        :type n: int

        :param without: Blacklist of words to not include in returned sample
        :type without: List[str]

        :return: Sample words
        :rtype: List[str]
        """
        return random.sample(
                [
                    word
                    for word in self.wordlist()
                    if word not in without
                    ],
                n
                )

    def wordlist(self) -> List[str]:
        """Returns list of unique words from vocabulary.

        :return: List of words
        :rtype: List[str]
        """
        return list(self.words.keys())
