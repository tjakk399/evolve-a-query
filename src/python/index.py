import logging

from typing import Dict, List, Optional

import elasticsearch
from elasticsearch.helpers import bulk

from query import Query
from vocabulary import Vocabulary

class Index():
    def __init__(
            self,
            name: str,
            host: str = "localhost",
            port: int = 9200,
            ):
        self.name = name

        self.es = elasticsearch.Elasticsearch(
                [
                    {
                        'host': host,
                        'port': port,
                        }
                    ],
                timeout = 300
                )

        self.vocabulary = Vocabulary()

        self.ensure_index()

    def ensure_index(self):
        request_body = {
            'settings' : {
                'number_of_shards': 2,
                'number_of_replicas': 1
                },
            'mappings': {
                'properties': {
                    'full_text': {
                        'type': 'text'
                        },
                    }
                }
            }

        try:
            logging.debug("Creating index")
            self.es.indices.create(
                    index = self.name,
                    body = request_body
                    )
        except elasticsearch.exceptions.RequestError:
            logging.debug("Deleting existing index")
            logging.debug(
                    self.es.indices.delete(
                        index = self.name,
                        )
                    )

        finally:
            try:
                self.es.indices.create(
                        index = self.name,
                        body = request_body
                        )

            except elasticsearch.exceptions.RequestError as e:
                logging.error(str(e))
                raise e

    def _bulk_data_generator(self, texts: List[str]):
        for text in texts:
            yield {
                    '_op_type': "index",
                    '_index': self.name,
                    # '_id': self.id,
                    '_source': {
                        'full_text': text,
                        },
                    }

    def add(self, text: str):
        self.vocabulary.add_words_from(text)

        return self.es.index(
                index = self.name,
                refresh = "wait_for",
                body = {
                    'full_text': text
                    },
                )

    def add_bulk(self, texts = List[str]):
        for text in texts:
            self.vocabulary.add_words_from(text)

        return bulk(
                client = self.es,
                actions = self._bulk_data_generator(texts),
                refresh = "wait_for",
                )


    def get(self, id: int):
        return self.es.get(
                index = self.name,
                id = id,
                )

    def search(self, query: Query):
        return self.es.search(
                index = self.name,
                body = query.body
                )

    def random_document(self):
        return self.es.search(
                index = self.name,
                body = {
                    'size': 1,
                    'query': {
                        'function_score': {
                            'query': {
                                'match_all': {}
                                },
                            'random_score': {}
                            }
                        }
                    }
                )

    def explain(self, query: Query, id: int):
        """Explanation for scoring"""
        return self.es.explain(
                index = self.name,
                id = id,
                body = query.body,
                )

