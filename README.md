# Invoice notification

This is a simple AWS Lambda function which is supposed to be enabled by cron and periodically run in the AWS.
It will scan an inbox on whether that contains a new mails and based on that sending an SNS message into the SNS
topic and further on as an SMS.

To run this Lambda function just create a new SNS topic:

```shell
aws sns create-topic --name invoice-notification
```

Also, please, check environment variables within the `app.py` and setup your environment variables in the AWS Lambda
console accordingly.