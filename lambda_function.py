import boto3
import datetime

# Change this if you want to increase/decrease the retention days of a snapshot.
RETENTION_DAYS = 7

def delete_snapshots():
    client = boto3.client('ec2')
    response = client.describe_snapshots(
        Filters=[
            {
                'Name': 'tag:created_by',
                'Values': [
                    'autosnapshot_bot',
                ]
            },
        ]
    )
    if 'Snapshots' in response:
        for snapshot in response['Snapshots']:
            delete_date = snapshot['StartTime'] + datetime.timedelta(days=RETENTION_DAYS)
            timenow = datetime.datetime.now(tz=datetime.timezone.utc)
            if timenow < delete_date:
                continue
            else:
                response = client.delete_snapshot(
                    SnapshotId=snapshot['SnapshotId'],
                )



def create_snapshots():
    client = boto3.client('ec2')
    response = client.describe_instances(
        Filters=[
            {
                'Name': 'tag:backup',
                'Values': [
                    'yes',
                ]
            },
        ]
    )
    if response:
        if 'Instances' in response['Reservations'][0]:
            for instances in response['Reservations']:
                instance = instances['Instances'][0]
                volId = instance['BlockDeviceMappings'][0]['Ebs']['VolumeId']
                snapshot = client.create_snapshot(
                    Description='{} - Snapshot Auto Created by AutoSnapBot'.format(instance['InstanceId']),
                    VolumeId=volId,
                    TagSpecifications=[
                        {
                            'ResourceType': 'snapshot',
                            'Tags': [
                                {
                                    'Key': 'created_by',
                                    'Value': 'autosnapshot_bot'
                                },
                            ]
                        },
                    ]
                )


def lambda_handler(event, context):
    create_snapshots()
    delete_snapshots()

