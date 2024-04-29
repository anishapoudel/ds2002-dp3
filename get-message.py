import boto3
from botocore.exceptions import ClientError
import requests
import json

queue_url = "https://sqs.us-east-1.amazonaws.com/440848399208/ap6acf"
sqs = boto3.client('sqs')

def delete_message(receipt_handle):
    sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)

def get_messages():
    messages = []
    while len(messages) < 10:
        response = sqs.receive_message(
            QueueUrl=queue_url,
            AttributeNames=['All'],
            MaxNumberOfMessages=1,
            MessageAttributeNames=['All'],
            WaitTimeSeconds=10 
        )
        if 'Messages' in response:
            for msg in response['Messages']:
                order = int(msg['MessageAttributes']['order']['StringValue'])
                word = msg['MessageAttributes']['word']['StringValue']
                messages.append((order, word))
                delete_message(msg['ReceiptHandle'])
        else:
            print("Waiting for messages...")

    # Sorting the messages by 'order'
    messages.sort()
    # Assembling the words into a phrase
    phrase = ' '.join(word for _, word in messages)
    # Output the phrase to a file
    with open('phrase.txt', 'w') as file:
        file.write(phrase)
    print("Phrase assembled and written to file.")

if __name__ == "__main__":
    get_messages()
