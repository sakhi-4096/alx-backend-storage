#!/usr/bin/env python3
"""
MongoDB aggregation script to find top students by average score.
"""


def top_students(mongo_collection):
    """
    Retrieve and return a list of students sorted by their average scores
    in descending order.

    Parameters:
    - mongo_collection: MongoDB collection object representing the students'
    data.
    Returns:
    A MongoDB aggregation result representing students and their average
    scores, sorted by average score in descending order.
    """
    return mongo_collection.aggregate([
        {
            "$project":
                {
                    "name": "$name",
                    "averageScore": {"$avg": "$topics.score"}
                }
        },
        {
            "$sort":
                {
                    "averageScore": -1
                }
        }
    ])
