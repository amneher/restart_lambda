import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    """
    AWS Lambda handler function.
    
    Args:
        event: The event dict containing request data
        context: The context object containing runtime information
        
    Returns:
        dict: Response with statusCode and body
    """
    logger.info(f"Received event: {json.dumps(event)}")
    
    try:
        body = {
            "message": "Hello from AWS Lambda!",
            "input": event
        }
        
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps(body)
        }
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({"error": str(e)})
        }
