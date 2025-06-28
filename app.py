import imaplib
import os

import boto3

client = boto3.client('sns')
topic_arn = os.environ["TOPIC_ARN"]


def lambda_handler(event, context):
    send_lease_notification()
    send_salary_notification()


def send_lease_notification():
    get_invoice_data(topic_arn,
                     'mail@mail.com',
                     'Invoice from ABC is here! It is the time to pay')


def send_salary_notification():
    get_invoice_data(topic_arn,
                     'payroll@mail.com',
                     'Salary is here it is the time to plan your budget, forecast and invest')


def get_invoice_data(arn, email, message):
    mail = imaplib.IMAP4_SSL(os.environ["IPAM_SERVER"])
    mail.login(os.environ["USERNAME"], os.environ["PASSWORD"])
    mail.select(readonly=True)
    result = mail.search(None, 'From', email)
    if result is not None:
        publish_notification(arn=arn, message=message)


def publish_notification(arn, message):
    client.publish(TargetArn=arn, Message=message)
