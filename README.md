# Invoice notification

This is a simple AWS Lambda function which is supposed to be enabled by cron and periodically run in the AWS.
It will scan an inbox on whether that contains a new mails and based on that sending an SNS message into the SNS
topic and further on as an SMS.

### How to run

1. Create a new SNS topic:

```shell
aws sns create-topic --name invoice-notification
```

2. Make a subscription towards that topic to send
   SMS [notifications](https://docs.aws.amazon.com/sns/latest/dg/sns-mobile-phone-number-as-subscriber.html)
3. Create a Lambda [function](https://docs.aws.amazon.com/lambda/latest/dg/getting-started.html)
4. Define all the environment variables that are called within the `app.py` within the Environment
   variables [page](https://docs.aws.amazon.com/lambda/latest/dg/configuration-envvars.html)
5. Make a Lambda function [scheduled](https://docs.aws.amazon.com/lambda/latest/dg/with-eventbridge-scheduler.html)