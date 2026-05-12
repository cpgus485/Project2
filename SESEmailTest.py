import boto3
import random
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    # Setting up connection to DynamoDB table
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('Project2WaterReminders')

    # Choosing a random reminder
    response = table.scan()
    reminder = random.choice(response['Items'])['reminder']

    # Setting up connection to SES
    ses = boto3.client('ses', region_name='us-east-1')

    # CHANGE EMAIL HERE
    SENDER = "YOUR_EMAIL@example.com"
    RECIPIENT = "YOUR_EMAIL@example.com"

    try:
        ses.send_email(
            Source=SENDER,
            Destination={'ToAddresses': [RECIPIENT]},
            Message={
                'Subject': {'Data': 'Water Reminder'},
                'Body': {'Text': {'Data': reminder}}
            }
        )
        print("Email sent successfully!")
    except ClientError as e:
        print("Error occurred:", e.response['Error']['Message'])