#!/usr/bin/env python3
"""
Return list of school having specific topic.
"""
import pymongo


def schools_by_topic(mongo_collection, topic):
    """
    Find specific topic
    """
    return mongo_collection.find({"topics":  {"$in": [topic]}})
