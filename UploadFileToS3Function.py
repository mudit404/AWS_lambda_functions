import json
import base64
import boto3
import uuid

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    try:
        # Determine where the file data is coming from
        if 'body' in event and event['body']:
            # If invoked via API Gateway
            is_base64_encoded = event.get('isBase64Encoded', False)
            if is_base64_encoded:
                body = json.loads(base64.b64decode(event['body']))
            else:
                body = json.loads(event['body'])
        else:
            # Direct invocation or test event
            body = event

        # Extract file data and bucket name
        file_data = body['file_data']  # Base64-encoded file data
        bucket_name = body['bucket_name']
        file_name = body.get('file_name', f"{uuid.uuid4()}.pdf")

        # Decode the base64 file data
        file_content = base64.b64decode(file_data)

        # Upload the file to S3
        s3_client.put_object(Bucket=bucket_name, Key=file_name, Body=file_content)

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'File uploaded successfully',
                'file_name': file_name
            })
        }

    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }
