import json
import boto3
import pandas as pd
import io
import os

# Initialize AWS clients
s3_client = boto3.client("s3")
bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

def lambda_handler(event, context):
    bucket = event.get("bucket")
    key = event.get("key")

    # Download file from S3
    obj = s3_client.get_object(Bucket=bucket, Key=key)
    df = pd.read_csv(io.BytesIO(obj['Body'].read()))

    # Convert first few rows to string for AI prompt
    sample_data = df.head(5).to_csv(index=False)

    # Prepare prompt
    prompt = f"""
    Analyze the following dataset and generate a normalized database schema up to BCNF.
    Dataset Sample:
    {sample_data}
    Provide tables with attributes and normalization steps clearly.
    """

    # Call AWS Bedrock model (Claude or Titan)
    response = bedrock.invoke_model(
        modelId="anthropic.claude-3-sonnet-20240229-v1:0",
        body=json.dumps({
            "prompt": prompt,
            "max_tokens": 800,
            "temperature": 0.5
        })
    )

    result = json.loads(response["body"].read())["completion"]
    return {
        "statusCode": 200,
        "body": json.dumps(result)
    }



