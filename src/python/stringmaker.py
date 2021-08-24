from __future__ import annotations

from typing import Dict, List, Optional, Set

from queries import Queries
from color import color


class StringMaker():
    def __init__(language: str = "en"):
        self.language = language

    @staticmethod
    def string(string: str) -> str:
        return string

    @staticmethod
    def delimiter(width: int = 80) -> str:
        return "=" * width

    @staticmethod
    def queries(queries: Queries) -> str:
        return "\n".join(
                [
                    "{:>5}. {:0<10} {}".format(
                        i + 1,
                        query.fitness,
                        query,
                        )
                    for i, query in enumerate(queries.sorted_queries())
                    ]
                )

    @staticmethod
    def actions(actions: List) -> str:
        return "\n".join(
                [
                    "[{}] {}\n\t{}\n".format(
                        i,
                        color.BOLD \
                                + actions[i].title \
                                + color.END,
                        actions[i].descr,
                        )
                    for i in range(
                        len(actions)
                        )
                    ]
                )

    @staticmethod
    def prompt_number(frm: int, to: int) -> str:
        return "Please type a number from {} to {}.".format(
                frm,
                to,
                )

    @staticmethod
    def section_title(title: str) -> str:
        return "{}\n{}\n{}".format(
                StringMaker.delimiter(),
                title,
                StringMaker.delimiter(),
                )

    @staticmethod
    def newline_delimited_list_of_titled_blocks(
            titled_blocks: List[Dict[str]]
            ) -> str:
        return "\n\n".join(
                [
                    "{}:\n{}".format(
                        titled_block["title"],
                        titled_block["block"],
                        )
                    for titled_block in titled_blocks
                    ]
                )

