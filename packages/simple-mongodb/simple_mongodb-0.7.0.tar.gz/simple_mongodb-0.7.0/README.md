# Simple-MongoDB

<p align="center">
    <img src="https://img.shields.io/badge/3.12-3b78a9?style=for-the-badge&logo=Python&logoColor=ffffff" alt="Supported-Python-Versions-Badge">
</p>

<p align="center">
    <a href="https://github.com/Gandori/Simple-MongoDB" target="_blank">
        <img src="https://img.shields.io/badge/Documentation-ef5552?style=for-the-badge&logo=Read the Docs&logoColor=ffffff" alt="Documentation-Badge">
    </a>
    <a href="https://github.com/Gandori/Simple-MongoDB" target="_blank">
        <img src="https://img.shields.io/badge/Source_code-0953dc?style=for-the-badge&logo=Github&logoColor=fffff" alt="Source-Code-Badge">
    </a>
    <a href="https://github.com/Gandori/Simple-MongoDB/blob/master/CHANGELOG.md" target="_blank">
        <img src="https://img.shields.io/badge/Changelog-3b78a9?style=for-the-badge&logo=Read the Docs&logoColor=ffffff" alt="Changelog-Badge">
    </a>
</p>

<p align="center">
    <a href="https://github.com/Gandori/Simple-MongoDB/blob/master/LICENSE" target="_blank">
        <img src="https://img.shields.io/github/license/Gandori/Simple-MongoDB?style=for-the-badge" alt="License-Badge">
    </a>
    <img src="https://img.shields.io/pypi/dm/simple-mongodb?style=for-the-badge&label=PyPi%20" alt="PyPi-Download-Badge">
    <a href="https://pypi.org/project/simple-mongodb/" target="_blank">
        <img src="https://img.shields.io/pypi/v/simple-mongodb?style=for-the-badge&color=%3b78a9&label=pypi%20package" alt="Package-version-Badge">
    </a>
    <img src="https://img.shields.io/github/actions/workflow/status/Gandori/Simple-MongoDB/publish.yml?&style=for-the-badge&label=Build%20Action" alt="Build-Action-Badge">
</p>

<p align="center">
    <img src="https://img.shields.io/github/created-at/Gandori/Simple-Mongodb?style=for-the-badge" alt="Created-Badge">
    <img src="https://img.shields.io/github/last-commit/Gandori/Simple-Mongodb?style=for-the-badge" alt="Last-Commit-Badge">
</p>

> Warning: This Python package is currently still in development phase

## Description

Placeholder

## Installation

```sh
pip install simple-mongodb
```

### Simple Example

```python
import asyncio
from typing import Any

from bson import ObjectId
from pydantic import BaseModel

from simple_mongodb import BaseCollection, MongoDBClient


class AccountCollection(BaseCollection):
    db = 'my-db'  # The name of the database or set the enviroment variable MONGODB_DB
    collection = 'account-collection'  # The name of the collection


class Account(BaseModel):
    name: str


async def main() -> None:
    # Initialize a client object and pass the url or set enviroment variables
    #   MONGODB_HOST, MONGODB_PORT,
    #   MONGODB_USERNAME, MONGODB_PASSWORD
    # Is the url param or enviroment variables not set the default values are used
    client: MongoDBClient = MongoDBClient(url='mongodb://user:pass@host:27017')

    # Initialize the account collection
    account_collection: AccountCollection = AccountCollection(client=client)

    account: Account = Account(name='example-name')

    try:

        # Insert the document in the collection
        document: dict[str, Any] = account.model_dump()
        inserted_id: ObjectId = await account_collection.insert_one(document=document)

        # Find the document
        where: dict[str, Any] = {'_id': inserted_id}
        document: dict[str, Any] = await account_collection.find_one(where=where)

        # Update the document
        update: dict[str, Any] = {'$set': {'name': 'other-name'}}
        # Returns the id of the new document if upsert=True
        await account_collection.update_one(where=where, update=update, upsert=False)

    except account_collection.InsertError:
        pass
    except account_collection.FindError:
        pass
    except account_collection.UpdateError:
        pass
    except account_collection.ServerTimeoutError:
        pass

    # Close the db connection
    client.close()


if __name__ == '__main__':
    asyncio.run(main())
```
