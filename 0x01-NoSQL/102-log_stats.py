#!/usr/bin/env python3
""" Provide statistics about Nginx logs stored in MongoDB."""
from pymongo import MongoClient


def nginx_stats_check():
    """
    This function connects to a MongoDB collection containing Nginx
    logs and prints various statistics, including the total number of
    logs, method-wise counts, status check count, and top IP addresses.

    Parameters:
    None
    Returns:
    None
    """
    # Connect to MongoDB
    client = MongoClient()
    collection = client.logs.nginx

    # Total number of logs
    num_of_docs = collection.count_documents({})
    print("{} logs".format(num_of_docs))

    # Method-wise counts
    print("Methods:")
    methods_list = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods_list:
        method_count = collection.count_documents({"method": method})
        print("\tmethod {}: {}".format(method, method_count))

    # Status check count
    status = collection.count_documents({"method": "GET", "path": "/status"})
    print("{} status check".format(status))

    # Top IP addresses
    print("IPs:")
    top_IPs = collection.aggregate([
        {"$group":
         {
             "_id": "$ip",
             "count": {"$sum": 1}
         }
         },
        {"$sort": {"count": -1}},
        {"$limit": 10},
        {"$project": {
            "_id": 0,
            "ip": "$_id",
            "count": 1
        }}
    ])
    for top_ip in top_IPs:
        count = top_ip.get("count")
        ip_address = top_ip.get("ip")
        print("\t{}: {}".format(ip_address, count))


if __name__ == "__main__":
    nginx_stats_check()
