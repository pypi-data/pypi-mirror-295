import pytest

from simple_mongodb import BaseCollection


def test_has_subclass_the_collection_value_not_implemented() -> None:
    with pytest.raises(ValueError):

        class ExampleCollection(BaseCollection):  # type: ignore
            pass


def test_is_collection_value_in_subclass_a_string() -> None:
    with pytest.raises(TypeError):

        class ExampleCollection(BaseCollection):  # type: ignore
            collection = 22  # type: ignore


def test_is_db_value_in_subclass_a_string() -> None:
    with pytest.raises(TypeError):

        class ExampleCollection(BaseCollection):  # type: ignore
            collection = 'example-collection'  # type: ignore
            db = 22  # type: ignore


def test_is_client_value_in_subclass() -> None:
    with pytest.raises(NotImplementedError):

        class ExampleCollection(BaseCollection):  # type: ignore
            collection = 'example-collection'  # type: ignore
            client = None  # type: ignore


def test_has_subclass_init_method() -> None:
    with pytest.raises(TypeError):

        class ExampleCollection(BaseCollection):  # type: ignore
            collection = 'example-collection'  # type: ignore

            def __init__(self) -> None:
                pass
