from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Literal


class BaseIndex(ABC):

    @abstractmethod
    def model_dump(self) -> dict[str, Any]:
        pass


class Index:
    @dataclass
    class SimpleIndex(BaseIndex):
        '''
        Represents a simple index on a single field.

        Attributes:
            index (str):
                The field name on which the index is created.
            name (str):
                Custom name to use for this index - if none is given, a name will be generated.
            sort (Literal[1, -1]):
                The sort order of the index, where 1 indicates ascending
                and -1 indicates descending. Default is 1.
            unique (bool):
                Specifies whether the index should enforce uniqueness. Default is False.
            sparse (bool):
                Specifies whether the index should only reference documents with the indexed
                field. Default is True.
            partialFilterExpression (None | dict[str, Any]):
                A filter expression to create a partial index. Default is None.
        '''

        index: str
        name: str | None = None
        sort: Literal[1, -1] = 1
        unique: bool = False
        sparse: bool = True
        partialFilterExpression: None | dict[str, Any] = None

        def model_dump(self) -> dict[str, Any]:
            return {
                'keys': [(self.index, self.sort)],
                'name': self.name,
                'unique': self.unique,
                'sparse': self.sparse,
                **(
                    {'partialFilterExpression': self.partialFilterExpression}
                    if self.partialFilterExpression
                    else {}
                ),
            }

    @dataclass
    class CompoundIndex(BaseIndex):
        '''
        Represents a compound index on multiple fields.

        Attributes:
            indexes (list[tuple[str, Literal[1, -1]]]):
                A list of tuples where each tuple contains a field name
                and the sort order (1 for ascending, -1 for descending).
            name (str):
                Custom name to use for this index - if none is given, a name will be generated.
            unique (bool):
                Specifies whether the index should enforce uniqueness. Default is False.
            sparse (bool):
                Specifies whether the index should only reference documents with all the indexed fields.
                Default is True.
            partialFilterExpression (None | dict[str, Any]):
                A filter expression to create a partial index. Default is None.
        '''

        indexes: list[tuple[str, Literal[1, -1]]]
        name: str | None = None
        unique: bool = False
        sparse: bool = True
        partialFilterExpression: None | dict[str, Any] = None

        def model_dump(self) -> dict[str, Any]:
            return {
                'keys': self.indexes,
                'name': self.name,
                'unique': self.unique,
                'sparse': self.sparse,
                **(
                    {'partialFilterExpression': self.partialFilterExpression}
                    if self.partialFilterExpression
                    else {}
                ),
            }

    @dataclass
    class TTLIndex(BaseIndex):
        '''
        Represents a TTL (Time To Live) index on a single field, used to automatically
        remove documents after a certain period.

        Attributes:
            index (str):
                The field name on which the TTL index is created.
            name (str):
                Custom name to use for this index - if none is given, a name will be generated.
            expireAfterSeconds (int):
                The number of seconds after which the documents will expire. Default is 3600.
            sort (Literal[1, -1]):
                The sort order of the index, where 1 indicates ascending
                and -1 indicates descending. Default is 1.
            sparse (bool):
                Specifies whether the index should only reference documents with the indexed
                field. Default is True.
            partialFilterExpression (None | dict[str, Any]):
                A filter expression to create a partial index. Default is None.
        '''

        index: str
        name: str | None = None
        expireAfterSeconds: int = 3600
        sort: Literal[1, -1] = 1
        sparse: bool = True
        partialFilterExpression: None | dict[str, Any] = None

        def model_dump(self) -> dict[str, Any]:
            return {
                'keys': [(self.index, self.sort)],
                'name': self.name,
                'sparse': self.sparse,
                **(
                    {'partialFilterExpression': self.partialFilterExpression}
                    if self.partialFilterExpression
                    else {}
                ),
            }

    IndexType = SimpleIndex | CompoundIndex | TTLIndex
