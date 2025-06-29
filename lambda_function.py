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
    publish_notification(topic_arn,
                         lease_email,
                         'Invoice from Qasa is here! It is the time to pay')

    publish_notification(topic_arn,
                         salary_email,
                         'Salary is here it is the time to plan your budget, forecast and invest')


def publish_notification(arn, email, message):
    result = find_unread_mail(email)

    if result is not None:
        publish(arn=arn, message=message)


def find_unread_mail(email):
    mail = imaplib.IMAP4_SSL(host=host, port=int(port))

    try:

        mail.login(username, password)
        mail.select('inbox')

        return mail.search(None, 'From', email, '(UNSEEN)')

    except Exception as e:
        raise Exception("Failed to authenticate", e)

    finally:
        mail.close()
        mail.logout()


def publish(arn, message):
    client.publish(TargetArn=arn, Message=message)
