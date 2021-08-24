from __future__ import annotations

from typing import Dict, List, Optional, Set

from collections import defaultdict

import random


class Vocabulary():
    def __init__(self, words: List(str) = []):
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
    def _tokenized(text: str):
        return text.split()

    def add_words(self, words):
        for word in words:
            self.words[word] += 1

    def add_words_from(self, text: str):
        self.add_words(Vocabulary._tokenized(text))

    def sample(self,
            n: int = 1,
            without: List[str] = []
            ) -> List[str]:
        return random.sample(
                [
                    word
                    for word in list(self.words.keys())
                    if word not in without
                    ],
                n
                )

    def wordlist(self):
        return list(self.words.keys())
