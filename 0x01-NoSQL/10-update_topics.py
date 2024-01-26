#!/usr/bin/env python3
"""
Change school topics based on the name.
"""
import pymongo


def update_topics(mongo_collection, name, topics):
    """
    Update document with a specific attr: value
    """
    return mongo_collection.update_many({
            "name": name
        },
        {
            "$set": {
                "topics": topics
            }
        })
