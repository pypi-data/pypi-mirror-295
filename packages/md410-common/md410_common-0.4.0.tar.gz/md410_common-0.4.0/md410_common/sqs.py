import boto3
from dotenv import load_dotenv

import json
import os

load_dotenv()

QUEUE_URL = os.getenv("AWS_QUEUE_URL")


SESSION = boto3.Session(
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)
SQS = SESSION.resource(
    "sqs",
    region_name=os.getenv("AWS_REGION", "af-south-1"),
)
QUEUE = SQS.Queue(QUEUE_URL)


def send_data(data: str, group_id: str = "default"):
    d = json.dumps(data)
    QUEUE.send_message(MessageBody=d, MessageGroupId=group_id)


def read_data(max_number_of_messages: int = 1, timeout: int = 5, delete: bool = True):
    results = QUEUE.receive_messages(
        AttributeNames=["All"],
        MaxNumberOfMessages=max_number_of_messages,
        WaitTimeSeconds=timeout,
    )
    output = []
    for r in results:
        output.append(
            {"type": r.attributes.get("MessageGroupId", "default"), "payload": r.body}
        )
        if delete:
            r.delete()
    return output


if __name__ == "__main__":
    if 0:
        send_data({"foo": "bar"})
    if 1:
        results = read_data(max_number_of_messages=5, delete=True)
        for res in results:
            print(res)
