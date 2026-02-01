"""Local test script for the Lambda function."""

from lambda_function import lambda_handler


class MockContext:
    """Mock AWS Lambda context object."""
    function_name = "test_function"
    function_version = "$LATEST"
    invoked_function_arn = "arn:aws:lambda:us-east-1:123456789012:function:test_function"
    memory_limit_in_mb = 128
    aws_request_id = "test-request-id"
    log_group_name = "/aws/lambda/test_function"
    log_stream_name = "test-log-stream"


def test_basic_invocation():
    """Test basic Lambda invocation."""
    event = {
        "key1": "value1",
        "key2": "value2"
    }
    
    response = lambda_handler(event, MockContext())
    
    print("Response:", response)
    assert response["statusCode"] == 200
    print("Basic invocation test passed!")


def test_api_gateway_event():
    """Test API Gateway proxy event."""
    event = {
        "httpMethod": "GET",
        "path": "/hello",
        "queryStringParameters": {"name": "World"},
        "headers": {"Content-Type": "application/json"},
        "body": None
    }
    
    response = lambda_handler(event, MockContext())
    
    print("API Gateway Response:", response)
    assert response["statusCode"] == 200
    print("API Gateway event test passed!")


if __name__ == "__main__":
    print("Running Lambda tests...\n")
    test_basic_invocation()
    print()
    test_api_gateway_event()
    print("\nAll tests passed!")
