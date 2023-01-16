import logging
import json
import bson
import os
from pymongo import MongoClient

MONGO_PW = os.environ['MONGO_PW']
WHATSAPP_KEY = os.environ['WHATSAPP_KEY']
MONGO_URL = "mongodb+srv://mongoun:{}@cluster0.cn2ieta.mongodb.net/?retryWrites=true&w=majority".format(MONGO_PW)

# Logger settings - CloudWatch
logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = MongoClient(MONGO_URL)
db = client.test


def handler(event, context):
    logger.info("Received event: " + json.dumps(event, indent=2))

    logger.info("initializing the collection")
    messages = db.messages

    logger.info("creating the user...")
    message = {
        "userId": event["userId"],
        "message": event["message"],
        "response": ""
    }
    message_id = messages.insert_one(message).inserted_id

    # Get created document from the database using ID.
    user = messages.find_one({"_id": message_id})

    return json.loads(json.dumps(user, default=json_unknown_type_handler))


def json_unknown_type_handler(x):
    """
    JSON cannot serialize decimal, datetime and ObjectId. So we provide this handler.
    """
    if isinstance(x, bson.ObjectId):
        return str(x)
    raise TypeError("Unknown datetime type")
