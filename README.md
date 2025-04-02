# AWS Lambda for EC2 Cost Optimization

This project sets up an AWS Lambda function to optimize EC2 usage costs. The primary use case is automatically starting and stopping EC2 instances used in the CI/CD pipeline based on specific tags. The function handles both starting and stopping of EC2 instances with designated tags.

## Scheduling

AWS EventBridge triggers the Lambda function based on the following schedule:

- **Stop:** `0 21 ? * MON-FRI *` → Every weekday at 9 PM  
- **Start:** `0 8 ? * MON-FRI *` → Every weekday at 8 AM  

## Permissions

To allow the Lambda function to start and stop EC2 instances, you must attach an appropriate IAM role with the necessary policy.

### IAM Policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "ec2:DescribeInstances",
        "ec2:DescribeTags"
      ],
      "Resource": "*",
      "Effect": "Allow"
    },
    {
      "Action": [
        "ec2:StartInstances",
        "ec2:StopInstances"
      ],
      "Resource": "arn:aws:ec2:*:*:instance/*",
      "Effect": "Allow"
    }
  ]
}
```

This policy grants the Lambda function permission to describe, start, and stop EC2 instances.
