#!/usr/bin/env python3
""" List all documents in Python collection. """
import pymongo


def list_all(mongo_collection):
    """
    List all documentation in a collection.
    """
    if not mongo_collection:
        return []
    documents = mongo_collection.find()
    return [post for post in documents]
