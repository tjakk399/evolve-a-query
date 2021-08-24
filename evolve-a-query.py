#!/usr/bin/env python3

import argparse
import json
import logging
import pathlib
import sys

sys.path.append("src/python")

from src.python.action import Action
from src.python.document import ESDocument
from src.python.index import Index
from src.python.queries import Queries
from src.python.query import Query
from src.python.stringmaker import StringMaker

logging.basicConfig(
        level = logging.ERROR
        )

def parsed_args():
    parser = argparse.ArgumentParser(
            description = "Evolve a query."
            )

    parser.add_argument(
            "language_file",
            type = pathlib.Path,
            action = "store",
            help = "path to language file with one sentence per line"
            )

    parser.add_argument(
            "--es-host",
            dest = "es_host",
            type = str,
            default = "localhost",
            action = "store",
            help = "host of Elasticsearch server"
            )

    parser.add_argument(
            "--es-port",
            dest = "es_port",
            type = int,
            default = 9200,
            action = "store",
            help = "port of Elasticsearch server",
            )

    parser.add_argument(
            "--n-rounds",
            dest = "n_rounds",
            type = int,
            default = 10,
            action = "store",
            help = "number of rounds to play",
            )

    parser.add_argument(
            "--n-lines-from-file",
            dest = "n_lines_from_file",
            type = int,
            default = None,
            action = "store",
            help = "number of lines from file to use for indexing (default: 0, all lines are used)",
            )

    return parser.parse_args()

def _actions(queries):
    return [
            Action(
                title = "Love Is In The Air",
                descr = "... but for now just clone each query once, doubling the population size.",
                func = queries.recombine,
                ),
            Action(
                title = "The Weak Shall Perish",
                descr = "Remove all queries whose scores match the worst score.",
                func = queries.select,
                ),
            Action(
                title = "Deus Ex Machina",
                descr = "Remove random queries from the population.",
                func = queries.random_purge,
                ),
            Action(
                title = "Gamma Party",
                descr = "Apply random mutations throughout the population. For each query, either a term will be removed or a random new term will be added with a random prefix (+/-).",
                func = queries.mutate,
                ),
            Action(
                title = "This Town Is Too Small For The Both Of Us",
                descr = "Remove duplicate queries.",
                func = queries.remove_duplicates,
                ),
            ]

def as_json(data):
    return json.dumps(
            data,
            indent = 4
            )

def read_lines(filepath):
    with open(filepath) as file:
        return [
                line.rstrip()
                for line in file.readlines()
                ]

def main():
    args = parsed_args()

    index = Index(
            name = "evolve_a_query",
            host = args.es_host,
            port = args.es_port,
            )

    index.add_bulk(
            read_lines(
                args.language_file
                )[0:args.n_lines_from_file]
            )

    logging.debug("index_info: " + as_json(index.es.info()))
    logging.debug("index_indices_mapping: " + as_json(index.es.indices.get_mapping()))

    target_sentence = ESDocument(
            index.random_document()
            )

    logging.debug("target_sentence: " + str(target_sentence))
    logging.debug("generating seed individual")

    queries = Queries(
            queries = [
                Query(
                    musts = index.vocabulary.sample(1)
                    )
                ],
            words = index.vocabulary.wordlist()
            )

    actions = _actions(queries)

    logging.debug("seed_query: " + str(queries.queries[0]))

    highscore = queries.average_score()

    for generation in [*range(args.n_rounds)]:
        logging.debug("computing fitness scores for each individual in population")

        for query in queries.queries:
            query.update_with_explanation(
                    index.explain(
                        query = query,
                        id = target_sentence.id
                        )
                    )

        logging.debug("presenting population with fitness scores")

        print(
                StringMaker.section_title(
                    "Generation " + str(generation + 1)
                    )
                )

        print(
                StringMaker.newline_delimited_list_of_titled_blocks(
                    [
                        {
                            'title': "Vocabulary",
                            'block': index.vocabulary,
                            },
                        {
                            'title': "Queries",
                            'block': StringMaker.queries(queries),
                            },
                        {
                            'title': "Average score (\"fitness\")",
                            'block': queries.average_score(),
                            },
                        {
                            'title': "Evolutionary actions",
                            'block': StringMaker.actions(actions),
                            },
                        ]
                    )
                )

        logging.debug("prompting for next action")

        action_number = None
        while action_number not in [*range(len(actions))]:
            try:
                action_number = int(
                        input(
                            "Which evolutionary action to take?\n> "
                            )
                        )

            except ValueError:
                print(StringMaker.prompt_number(
                    0,
                    len(actions)-1)
                    )

        logging.debug("performing action on population")

        actions[action_number].func()

        logging.debug("target_sentence: " + str(target_sentence))

        score = queries.average_score()

        if highscore < score:
            highscore = score

        if queries.size() == 0:
            print(
                    StringMaker.string(
                        "Your queries died out. You lost. Game over."
                        )
                    )
            break

    print(StringMaker.delimiter())

    print(
            StringMaker.newline_delimited_list_of_titled_blocks(
                [
                    {
                        'title': "Best average score",
                        'block': str(highscore),
                        },
                    {
                        'title': "Target sentence",
                        'block': str(target_sentence),
                        },
                    {
                        'title': "Last queries",
                        'block': StringMaker.queries(queries),
                        },
                    ]
                )
            )

if __name__ == "__main__":
    main()
