import imaplib
import os

import boto3

client = boto3.client('sns')
topic_arn = os.environ["TOPIC_ARN"]
imap_server = os.environ["IPAM_SERVER"]
imap_port = os.environ["IMAP_PORT"]
mail_username = os.environ["USERNAME"]
mail_password = os.environ["PASSWORD"]


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
    mail = imaplib.IMAP4_SSL(host=imap_server, port=int(imap_port))

    mail.login(mail_username, mail_password)
    mail.select(readonly=True)

    result = mail.search(None, 'From', email)
    if result is not None:
        publish_notification(arn=arn, message=message)

    mail.close()
    mail.logout()


def publish_notification(arn, message):
    client.publish(TargetArn=arn, Message=message)
