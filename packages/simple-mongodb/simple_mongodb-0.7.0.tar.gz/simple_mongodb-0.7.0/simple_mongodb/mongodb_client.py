import os
from functools import wraps
from typing import Any, Callable, Dict, List, Literal

from bson import ObjectId
from motor.core import AgnosticCursor
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import IndexModel
from pymongo.errors import DuplicateKeyError, ServerSelectionTimeoutError
from pymongo.results import (
    DeleteResult,
    InsertManyResult,
    InsertOneResult,
    UpdateResult,
)

from .exceptions import Exceptions
from .index import Index


def exception_decorator(
    exception: type[Exception],
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return await func(*args, **kwargs)
            except DuplicateKeyError as e:
                print(e)
                raise Exceptions.DuplicateKeyError(e)
            except ServerSelectionTimeoutError as e:
                print(e)
                raise Exceptions.ServerTimeoutError(e)
            except Exception as e:
                print(e)
                raise exception(e)

        return wrapper

    return decorator


class MongoDBClient:
    def __init__(
        self,
        url: str | None = None,
        host: str | None = None,
        port: int | None = None,
        username: str | None = None,
        password: str | None = None,
        db: str | None = None,
        response_timeout: int | None = None,
        connection_timeout: int | None = None,
    ) -> None:
        self.url: str
        self.host: str
        self.port: int
        self.username: str
        self.password: str
        self.response_timeout: int
        self.connection_timeout: int
        self.db: str = db if db else os.getenv('MONGODB_DB', 'example')

        if not url:
            self.host = host if host else os.getenv('MONGODB_HOST', 'localhost')

            try:
                self.port = port if port else int(os.getenv('MONGODB_PORT', '27017'))
            except ValueError:
                raise ValueError('MONGODB_PORT must be a int')

            self.username = (
                username if username else os.getenv('MONGODB_USERNAME', 'user')
            )
            self.password = (
                password if password else os.getenv('MONGODB_PASSWORD', 'user')
            )

            self.url = (
                f'mongodb://{self.username}:{self.password}@{self.host}:{self.port}'
            )
        else:
            self.url = url

        try:
            self.response_timeout = (
                response_timeout
                if response_timeout
                else int(os.getenv('MONGODB_RESPONSE_TIMEOUT', '5000'))
            )
        except ValueError:
            raise ValueError('MONGODB_RESPONSE_TIMEOUT must be a int')

        try:
            self.connection_timeout = (
                connection_timeout
                if connection_timeout
                else int(os.getenv('MONGODB_CONNECTION_TIMEOUT', '5000'))
            )
        except ValueError:
            raise ValueError('MONGODB_CONNECTION_TIMEOUT must be a int')

        self.__client: AsyncIOMotorClient[Any] = AsyncIOMotorClient(
            self.url,
            serverSelectionTimeoutMS=self.response_timeout,
            connectTimeoutMS=self.connection_timeout,
        )

    def close(self) -> None:
        self.__client.close()

    @exception_decorator(exception=Exceptions.FindError)
    async def find_one(
        self, db: str, collection: str, where: dict[str, Any]
    ) -> Dict[str, Any]:
        result: dict[str, Any] | None = await self.__client[db][collection].find_one(
            where
        )
        if not result:
            raise Exceptions.NotFoundError('The document was not found')
        return result

    @exception_decorator(exception=Exceptions.FindError)
    async def find(
        self,
        db: str,
        collection: str,
        where: dict[str, Any] = {},
        skip: int = 0,
        limit: int = 25,
        sort: list[tuple[str, Literal[-1, 1]]] | None = None,
    ) -> List[Dict[str, Any]]:
        cursor: AgnosticCursor[Any] = self.__client[db][collection].find(where)
        if sort is None:
            return await cursor.skip(skip=skip).to_list(length=limit)  # type: ignore
        return await cursor.sort(sort).skip(skip=skip).to_list(length=limit)  # type: ignore

    @exception_decorator(exception=Exceptions.InsertError)
    async def insert_one(
        self, db: str, collection: str, document: dict[str, Any]
    ) -> ObjectId:
        result: InsertOneResult = await self.__client[db][collection].insert_one(
            document
        )
        return result.inserted_id

    @exception_decorator(exception=Exceptions.InsertError)
    async def insert_many(
        self,
        db: str,
        collection: str,
        documents: List[Dict[str, Any]],
        ordered: bool = True,
        bypass_document_validation: bool = False,
    ) -> List[ObjectId]:
        result: InsertManyResult = await self.__client[db][collection].insert_many(
            documents=documents,
            ordered=ordered,
            bypass_document_validation=bypass_document_validation,
        )
        return result.inserted_ids

    @exception_decorator(exception=Exceptions.UpdateError)
    async def update_one(
        self,
        db: str,
        collection: str,
        where: dict[str, Any],
        update: dict[str, Any],
        upsert: bool = False,
    ) -> ObjectId | None:
        result: UpdateResult = await self.__client[db][collection].update_one(
            filter=where, update=update, upsert=upsert
        )
        return result.upserted_id

    @exception_decorator(exception=Exceptions.DeleteError)
    async def delete_one(self, db: str, collection: str, where: dict[str, Any]) -> int:
        result: DeleteResult = await self.__client[db][collection].delete_one(where)
        return result.deleted_count

    @exception_decorator(exception=Exceptions.DeleteError)
    async def delete_many(self, db: str, collection: str, where: dict[str, Any]) -> int:
        result: DeleteResult = await self.__client[db][collection].delete_many(
            filter=where
        )
        return result.deleted_count

    @exception_decorator(exception=Exceptions.DropCollectionError)
    async def drop_collection(self, db: str, collection: str) -> None:
        await self.__client[db][collection].drop()

    @exception_decorator(exception=Exceptions.CountDocumentsError)
    async def count_documents(
        self, db: str, collection: str, where: dict[str, Any]
    ) -> int:
        return await self.__client[db][collection].count_documents(filter=where)

    @exception_decorator(exception=Exceptions.CreateIndexError)
    async def create_index(
        self, db: str, collection: str, index: Index.IndexType
    ) -> None:
        await self.__client[db][collection].create_index(**index.model_dump())

    @exception_decorator(exception=Exceptions.CreateIndexError)
    async def create_indexes(
        self, db: str, collection: str, indexes: list[Index.IndexType]
    ) -> None:
        await self.__client[db][collection].create_indexes(
            indexes=[IndexModel(**index.model_dump()) for index in indexes]
        )
