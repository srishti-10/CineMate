import os
from pymongo import MongoClient

# Get MongoDB connection details from environment variables or use defaults
MONGO_HOST = os.getenv('MONGO_HOST', 'localhost')
MONGO_PORT = int(os.getenv('MONGO_PORT', 27017))

# Function to get a MongoDB client
# Use this function wherever you need to interact with MongoDB

def get_mongo_client():
    """
    Returns a MongoClient instance connected to the specified host and port.
    """
    return MongoClient(host=MONGO_HOST, port=MONGO_PORT) 