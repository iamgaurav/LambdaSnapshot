# Lambda Snapshot BOT

This is an AWS Lambda bot which lets you create EC2 snapshots and also deletes the older
snapshots based on the creation date of the snapshot. 


# Config Variables

Changing the following variable `RETENTION_DAYS` value in lambda_function.py 
lets you control the number of days you want to retain a snashot. 

By default this value is set to 7 i.e 7 Days a snapshot will be retained.

# Setup 

### Enable Backups

To enable auto backups on an EC2 instance you need to attach the following tag 
to any EC2 instance you want to backup.

```
key: backup
value: yes
```

### AWS Console

The bot requires the following permissions to function. 
Create an execution role with the following policy template.

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:*"
            ],
            "Resource": "arn:aws:logs:*:*:*"
        },
        {
            "Effect": "Allow",
            "Action": "ec2:Describe*",
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "ec2:CreateSnapshot",
                "ec2:DeleteSnapshot",
                "ec2:CreateTags",
                "ec2:ModifySnapshotAttribute",
                "ec2:ResetSnapshotAttribute"
            ],
            "Resource": [
                "*"
            ]
        }
    ]
}
```

#### Cloud Watch Events

Once the lambda excution role is created and attached to the lambda function in AWS, a Cloud Watch cron event
needs to be created to execute this function every day once.

Create a new rule and add the following schedule expression:
`0 23 * * ? *`

