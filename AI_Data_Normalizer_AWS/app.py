import streamlit as st
import boto3
import pandas as pd
import pymysql
import io
import os
from sqlalchemy import create_engine, text

# --- AWS Configuration ---
S3_BUCKET = "your-s3-bucket-name"
LAMBDA_FUNCTION = "your-lambda-function-name"
RDS_HOST = "your-rds-endpoint.amazonaws.com"
RDS_USER = "your-db-username"
RDS_PASSWORD = "your-db-password"
RDS_DB = "your-database-name"
REGION = "us-east-1"  # change as needed

# --- Initialize AWS clients ---
s3_client = boto3.client('s3', region_name=REGION)
lambda_client = boto3.client('lambda', region_name=REGION)

# --- Streamlit UI ---
st.title("AI Data Normalization System (AWS)")

uploaded_file = st.file_uploader("Upload your CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file is not None:
    st.success("File uploaded successfully!")

    # Read file
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.dataframe(df.head())

    # Upload to S3
    s3_key = f"uploads/{uploaded_file.name}"
    with io.BytesIO() as buffer:
        df.to_csv(buffer, index=False)
        buffer.seek(0)
        s3_client.upload_fileobj(buffer, S3_BUCKET, s3_key)
    st.info(f"File uploaded to S3 bucket: `{S3_BUCKET}`")

    # Call Lambda (Bedrock-powered)
    if st.button("Normalize Data with AI"):
        payload = {
            "bucket": S3_BUCKET,
            "key": s3_key,
        }
        response = lambda_client.invoke(
            FunctionName=LAMBDA_FUNCTION,
            InvocationType="RequestResponse",
            Payload=str(payload).encode("utf-8"),
        )

        result = response["Payload"].read().decode("utf-8")
        st.success("AI Normalization Completed")
        st.code(result)

        # Save to RDS MySQL
        try:
            engine = create_engine(
                f"mysql+pymysql://{RDS_USER}:{RDS_PASSWORD}@{RDS_HOST}/{RDS_DB}"
            )
            with engine.connect() as conn:
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS normalization_results (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        file_name VARCHAR(255),
                        normalized_schema TEXT
                    )
                """))
                conn.execute(
                    text("INSERT INTO normalization_results (file_name, normalized_schema) VALUES (:file, :schema)"),
                    {"file": uploaded_file.name, "schema": result}
                )
            st.info("Results saved to RDS MySQL")
        except Exception as e:
            st.error(f"Database error: {e}")
















