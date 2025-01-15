import json

def lambda_handler(event, context):
    try:
        # Determine where the numbers are coming from
        if 'queryStringParameters' in event and event['queryStringParameters']:
            # If invoked via API Gateway with query parameters
            number1 = float(event['queryStringParameters'].get('number1', 0))
            number2 = float(event['queryStringParameters'].get('number2', 0))
        elif 'body' in event and event['body']:
            # If numbers are in the request body
            body = json.loads(event['body'])
            number1 = float(body.get('number1', 0))
            number2 = float(body.get('number2', 0))
        else:
            # Direct invocation or test event
            number1 = float(event.get('number1', 0))
            number2 = float(event.get('number2', 0))
        
        result = number1 + number2

        return {
            'statusCode': 200,
            'body': json.dumps({'result': result})
        }

    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }
