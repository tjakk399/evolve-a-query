from __future__ import annotations

from typing import Dict, List, Optional, Set

import json

class ESDocument():
    def __init__(self, document: Dict):
        self._document = document

        self.id = self.id()

    def __str__(self) -> str:
        return self._document['hits']['hits'][0]['_source']['full_text']

    def __repr__(self) -> str:
        return json.dumps(
                self._document,
                indent = 4
                )

    def id(self) -> int:
        return self._document['hits']['hits'][0]['_id']

