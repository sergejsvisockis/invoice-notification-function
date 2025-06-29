# Invoice notification

This is a simple AWS Lambda function which is supposed to be enabled by cron and periodically run in the AWS.
It will scan an inbox on whether that contains a new mails and based on that sending an SNS message into the SNS
topic and further on as an SMS.

### Deployment

1. Follow
   these [steps](https://docs.aws.amazon.com/lambda/latest/dg/python-package.html#python-package-create-dependencies)
2. Create an IAM role

```shell
aws iam create-role \
--role-name invoice-notification-lambda \
--assume-role-policy-document file://trust-policy.json
```

3. Grant a full to a SNS for that role

```shell
aws iam put-role-policy \
--role-name invoice-notification-lambda \
--policy-name LambdaSNSFullAccess \
--policy-document file://sns-full-access.json
```

4. Deploy Lambda function

```shell
aws lambda create-function --function-name invoice-notification-function \
--runtime python3.13 --handler lambda_function.lambda_handler \
--role arn:aws:iam::117863533677:role/invoice-notification-lambda \
--zip-file fileb://invoice-notification-function.zip
```

5. Add all th necessary environment variables

```shell
aws lambda update-function-configuration \
--function-name invoice-notification-function \
--environment "Variables={TOPIC_ARN=VALUE,IMAP_SERVER=VALUE,IMAP_PORT=VALUE,LEASE_EMAIL=VALUE,SALARY_EMAIL=VALUE,USERNAME=VALUE,PASSWORD=VALUE}"
```

5. Add a trigger in the EventBridge. That could be done in the AWS Console UI within the Lambda configuration.

6. Create a new SNS topic:

```shell
aws sns create-topic --name invoice-notification
```

7. Create a subscription via the SMS to send an SMS notifications. NOTE: AWS has a limit on how many SMS notifications
   could be made on the monthly basis. Please, check your billing plan.