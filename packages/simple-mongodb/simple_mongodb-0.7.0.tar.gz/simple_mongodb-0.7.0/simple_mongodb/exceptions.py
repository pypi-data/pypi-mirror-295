class Exceptions:
    '''
    A base class for custom exceptions related to database operations.
    '''

    class FindError(Exception):
        '''
        Raised when an error occurs while finding documents.
        '''

        pass

    class FindOneError(Exception):
        '''
        Raised when an error occurs while finding a single document.
        '''

        pass

    class NotFoundError(Exception):
        '''
        Raised when a document is not found.
        '''

        pass

    class InsertError(Exception):
        '''
        Raised when an error occurs while inserting a document.
        '''

        pass

    class DuplicateKeyError(Exception):
        '''
        Raised when a duplicate key error occurs while inserting a document.
        '''

        pass

    class AggregateError(Exception):
        '''
        Raised when an error occurs during document aggregation.
        '''

        pass

    class UpdateError(Exception):
        '''
        Raised when an error occurs while updating a document.
        '''

        pass

    class DeleteError(Exception):
        '''
        Raised when an error occurs while deleting a document.
        '''

        pass

    class CreateIndexError(Exception):
        '''
        Raised when an error occurs while creating an index.
        '''

        pass

    class DropIndexError(Exception):
        '''
        Raised when an error occurs while dropping an index.
        '''

        pass

    class ServerTimeoutError(Exception):
        '''
        Raised when a server timeout error occurs.
        '''

        pass

    class DropCollectionError(Exception):
        '''
        Raised when an error occurs while dropping a collection.
        '''

        pass

    class CountDocumentsError(Exception):
        '''
        Raised when an error occurs while counting documents in the collection.
        '''

        pass
