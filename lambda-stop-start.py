import boto3
import os

def lambda_handler(event, context):
    if "action" not in event:
        return {"status": "error", "message": "Missing required parameter: action"}

    action = event["action"]  # No default value

    tag_key = os.getenv("TAG_KEY", "Name")
    tag_value = os.getenv("TAG_VALUE", "website")
    ec2 = boto3.client('ec2')
    
    # Filter instances by the provided tag key and value
    filters = [
        {
            'Name': f'tag:{tag_key}',
            'Values': [tag_value]
        }
    ]
    
    try:
        # Describe instances based on tag filters
        instances = ec2.describe_instances(Filters=filters)
        
        # Extract instance IDs from the response
        instance_ids = [instance['InstanceId'] for reservation in instances['Reservations'] for instance in reservation['Instances']]
        
        if not instance_ids:
            return {"status": "error", "message": f"No instances found with tag {tag_key}: {tag_value}"}
        
        # Perform the requested action (start or stop)
        if action == "start":
            ec2.start_instances(InstanceIds=instance_ids)
            return {"status": "success", "message": f"Started instances: {instance_ids}"}
        elif action == "stop":
            ec2.stop_instances(InstanceIds=instance_ids)
            return {"status": "success", "message": f"Stopped instances: {instance_ids}"}
        else:
            return {"status": "error", "message": "Invalid action specified"}
    
    except Exception as e:
        return {"status": "error", "message": str(e)}
