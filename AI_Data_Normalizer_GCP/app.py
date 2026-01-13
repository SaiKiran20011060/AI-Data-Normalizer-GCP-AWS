import streamlit as st
from google.cloud import storage
from google.cloud.sql.connector import Connector
import sqlalchemy
import pandas as pd
import io
import os
import google.generativeai as genai

# -------------- CONFIGURATION --------------
PROJECT_ID = "your-gcp-project-id"
BUCKET_NAME = "your-gcs-bucket-name"
INSTANCE_CONNECTION_NAME = "your-project:your-region:your-instance"
DB_USER = "your-db-username"
DB_PASS = "your-db-password"
DB_NAME = "your-database-name"
GEMINI_API_KEY = "your-gemini-api-key"

# Initialize Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Initialize GCS client
storage_client = storage.Client(project=PROJECT_ID)

# Initialize Cloud SQL Connector
connector = Connector()

def getconn():
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pymysql",
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME
    )
    return conn

pool = sqlalchemy.create_engine(
    "mysql+pymysql://",
    creator=getconn,
)

# -------------- STREAMLIT UI --------------
st.title("AI Data Normalization System (GCP)")
st.write("Upload your dataset and let Gemini AI create a normalized database schema (up to BCNF).")

uploaded_file = st.file_uploader("Upload your CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file is not None:
    st.success("File uploaded successfully!")

    # Read the uploaded file
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.dataframe(df.head())

    # Upload file to GCS
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(f"uploads/{uploaded_file.name}")

    with io.BytesIO() as buffer:
        df.to_csv(buffer, index=False)
        buffer.seek(0)
        blob.upload_from_file(buffer, content_type="text/csv")

    st.info(f"File uploaded to GCS: `{BUCKET_NAME}/uploads/{uploaded_file.name}`")

    # Trigger Gemini for normalization
    if st.button("Normalize Data with AI"):
        try:
            sample_data = df.head(5).to_csv(index=False)
            prompt = f"""
            You are a database normalization expert.
            Given this dataset sample, generate a normalized schema up to BCNF.
            Include table names, attributes, primary/foreign keys, and a brief normalization explanation.
            Dataset sample:
            {sample_data}
            """

            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(prompt)

            normalized_schema = response.text
            st.success("Normalization completed successfully!")
            st.code(normalized_schema, language="sql")

            # Save result to Cloud SQL
            with pool.connect() as conn:
                conn.execute(sqlalchemy.text("""
                    CREATE TABLE IF NOT EXISTS normalization_results (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        file_name VARCHAR(255),
                        normalized_schema TEXT
                    )
                """))
                conn.execute(
                    sqlalchemy.text("INSERT INTO normalization_results (file_name, normalized_schema) VALUES (:file, :schema)"),
                    {"file": uploaded_file.name, "schema": normalized_schema}
                )
            st.info("Results saved to Cloud SQL database")

        except Exception as e:
            st.error(f"Error: {e}")




