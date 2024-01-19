"""
Copyright (c) 2023 Combo Gang. All rights reserved.

This work is licensed under the terms of the MIT license.  
For a copy, see <https://opensource.org/licenses/MIT>.
"""
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.results import InsertOneResult, UpdateResult, DeleteResult
from typing import Optional, List, Union, Dict, Any


class MongoDBUtility:
    """
    Initialize the MongoDBUtility.

    Params
    ---------
    @param connection (str | MongoClient): MongoDB connection string or MongoClient instance.
    @param database_name (str): Name of the MongoDB database.

    Returns
    ---------
    @returns None: No return value.
    """

    def __init__(self, connection: str | MongoClient, database_name: str) -> None:
        self.client = (
            connection
            if isinstance(connection, MongoClient)
            else MongoClient(connection)
        )
        self.database = self.client[database_name]

    """
    Insert a document into the specified collection.

    Params
    ---------
    @param collection_name (str): Name of the MongoDB collection.
    @param document (Dict[str, Any]): Document to be inserted.

    Returns
    ---------
    @returns Any: The ID of the inserted document.
    """

    def insert_document(self, collection_name: str, document: Dict[str, Any]) -> Any:
        collection: Collection = self.database[collection_name]
        result: InsertOneResult = collection.insert_one(document)
        return result.inserted_id

    """
    Find documents in the specified collection based on the query.

    Params
    ---------
    @param collection_name (str): Name of the MongoDB collection.
    @param query (Optional[Dict[str, Any]]): Query to filter documents.
    @param projection (Optional[Dict[str, Union[int, bool]]]): Fields to include/exclude in the result.

    Returns
    ---------
    @returns List[Dict[str, Any]]: List of documents matching the query.
    """

    def find_documents(
        self,
        collection_name: str,
        query: Optional[Dict[str, Any]] = None,
        projection: Optional[Dict[str, Union[int, bool]]] = None,
    ) -> List[Dict[str, Any]]:
        collection: Collection = self.database[collection_name]
        cursor = collection.find(query, projection)
        return list(cursor)

    """
    Find one document in the specified collection based on the query.

    Params
    ---------
    @param collection_name (str): Name of the MongoDB collection.
    @param query (Optional[Dict[str, Any]]): Query to filter documents.
    @param projection (Optional[Dict[str, Union[int, bool]]]): Fields to include/exclude in the result.

    Returns
    ---------
    @returns Optional[Dict[str, Any]]: The first document matching the query, or None if not found.
    """

    def find_one_document(
        self,
        collection_name: str,
        query: Optional[Dict[str, Any]] = None,
        projection: Optional[Dict[str, Union[int, bool]]] = None,
    ) -> Optional[Dict[str, Any]]:
        collection: Collection = self.database[collection_name]
        return collection.find_one(query, projection)

    """
    Update documents in the specified collection based on the query.

    Params
    ---------
    @param collection_name (str): Name of the MongoDB collection.
    @param query (Dict[str, Any]): Query to filter documents to be updated.
    @param update (Dict[str, Any]): Update operation to be applied.

    Returns
    ---------
    @returns int: The number of documents modified.
    """

    def update_document(
        self, collection_name: str, query: Dict[str, Any], update: Dict[str, Any]
    ) -> int:
        collection: Collection = self.database[collection_name]
        result: UpdateResult = collection.update_one(query, {"$set": update})
        return result.modified_count

    """
    Delete documents in the specified collection based on the query.

    Params
    ---------
    @param collection_name (str): Name of the MongoDB collection.
    @param query (Dict[str, Any]): Query to filter documents to be deleted.

    Returns
    ---------
    @returns int: The number of documents deleted.
    """

    def delete_document(self, collection_name: str, query: Dict[str, Any]) -> int:
        collection: Collection = self.database[collection_name]
        result: DeleteResult = collection.delete_one(query)
        return result.deleted_count

    """
    Find one document in the specified collection based on the query and update it.

    Params
    ---------
    @param collection_name (str): Name of the MongoDB collection.
    @param query (Dict[str, Any]): Query to filter documents to be updated.
    @param update (Dict[str, Any]): Update operation to be applied.

    Returns
    ---------
    @returns Optional[Dict[str, Any]]: The updated document.
    """

    def find_document_and_update(
        self, collection_name: str, query: Dict[str, Any], update: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        collection: Collection = self.database[collection_name]
        return collection.find_one_and_update(query, {"$set": update})

    """
    Find one document in the specified collection based on the ID.

    Params
    ---------
    @param collection_name (str): Name of the MongoDB collection.
    @param _id (str): ID of the document to be found.
    @param projection (Optional[Dict[str, Union[int, bool]]]): Fields to include/exclude in the result.

    Returns
    ---------
    @returns Optional[Dict[str, Any]]: The document matching the ID, or None if not found.
    """

    def find_document_by_id(
        self,
        collection_name: str,
        _id: str,
        projection: Optional[Dict[str, Union[int, bool]]] = None,
    ) -> Optional[Dict[str, Any]]:
        collection: Collection = self.database[collection_name]
        return collection.find_one({"_id": _id}, projection)

    """
    Insert a document into the specified collection if it does not exist.

    Params
    ---------
    @param collection_name (str): Name of the MongoDB collection.
    @param document (Dict[str, Any]): Document to be inserted.

    Returns
    ---------
    @returns Any: The ID of the inserted document.
    """

    def insert_document_if_not_exists(
        self, collection_name: str, document: Dict[str, Any]
    ) -> Any:
        collection: Collection = self.database[collection_name]
        result: InsertOneResult = collection.update_one(
            document, {"$setOnInsert": document}, upsert=True
        )
        return result.upserted_id

    """
    Update a document in the specified collection if it exists.

    Params
    ---------
    @param collection_name (str): Name of the MongoDB collection.
    @param query (Dict[str, Any]): Query to filter documents to be updated.
    @param update (Dict[str, Any]): Update operation to be applied.

    Returns
    ---------
    @returns int: The number of documents modified.
    """

    def update_document_if_exists(
        self, collection_name: str, query: Dict[str, Any], update: Dict[str, Any]
    ) -> int:
        collection: Collection = self.database[collection_name]
