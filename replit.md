# AWS Lambda Python Boilerplate

## Overview
A simple AWS Lambda function boilerplate in Python 3.12.

## Project Structure
- `lambda_function.py` - Main Lambda handler function
- `test_lambda.py` - Local testing script

## How to Use

### Local Testing
Run the test script to verify the Lambda function works:
```
python test_lambda.py
```

### Deploying to AWS
1. Zip the `lambda_function.py` file
2. Upload to AWS Lambda console or use AWS CLI/SAM

## Lambda Handler
The handler is configured as `lambda_function.lambda_handler`.
