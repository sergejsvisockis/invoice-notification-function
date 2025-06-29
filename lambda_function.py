import imaplib
import os

import boto3

client = boto3.client('sns')
topic_arn = os.getenv('TOPIC_ARN')

host = os.getenv('IMAP_SERVER')
port = os.getenv('IMAP_PORT')
password = os.getenv('PASSWORD')
username = os.getenv('USERNAME')
lease_email = os.getenv('LEASE_EMAIL')
salary_email = os.getenv('SALARY_EMAIL')


def lambda_handler(event, context):
    send_lease_notification()
    send_salary_notification()


def send_lease_notification():
    get_invoice_data(topic_arn,
                     lease_email,
                     'Invoice from Qasa is here! It is the time to pay')


def send_salary_notification():
    get_invoice_data(topic_arn,
                     salary_email,
                     'Salary is here it is the time to plan your budget, forecast and invest')


def get_invoice_data(arn, email, message):
    mail = imaplib.IMAP4_SSL(host=host, port=int(port))

    try:

        mail.login(username, password)
        mail.select('inbox')

        result = mail.search(None, 'From', email, '(UNSEEN)')
        if result is not None:
            publish_notification(arn=arn, message=message)

    except Exception as e:
        raise Exception("Failed to authenticate", e)

    finally:
        mail.close()
        mail.logout()


def publish_notification(arn, message):
    client.publish(TargetArn=arn, Message=message)
