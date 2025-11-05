# 🧠 AI Data Normalization System (AWS & GCP)

An AI-powered web application that automates **data normalization** up to BCNF using **Streamlit**, **Python**, and cloud-based AI models.  
It supports **both AWS (Bedrock)** and **GCP (Gemini AI)** architectures for flexibility and scalability.

---

## 🚀 Project Overview

The app allows users to:
- Upload raw **CSV or Excel** files.
- Automatically store them in **S3 (AWS)** or **GCS (GCP)**.
- Trigger an **AI model** (Bedrock on AWS or Gemini on GCP) to analyze and generate **normalized database schemas**.
- Store and manage normalized results in **RDS (AWS)** or **Cloud SQL (GCP)**.
- Display clean, readable results via a **Streamlit web interface**.

---

## 🌩️ Architecture Comparison

### **AWS Architecture**
- **Streamlit + Python (UI):** User interface for file upload and schema visualization.
- **Amazon S3:** Stores uploaded datasets.
- **AWS Lambda:** Executes AI normalization logic when triggered.
- **Amazon Bedrock (Claude/Sonnet):** Generates normalized database schemas.
- **Amazon RDS (MySQL):** Persists normalized schema results.

### **GCP Architecture**
- **Streamlit + Python (UI):** Same as AWS version.
- **Google Cloud Storage (GCS):** Stores uploaded files.
- **Gemini AI (via API Key):** Generates normalized schemas and explanations.
- **Cloud SQL (MySQL):** Saves normalized outputs for future reference.

---


##🧠 AI Normalization Logic

Both architectures follow a similar AI logic:

Extract sample data from uploaded file.

Send prompt to AI model describing dataset.

AI generates normalized schema (1NF → 3NF → BCNF).

Save results in respective SQL databases.

Display schema and explanation in Streamlit UI.

##📊 Key Features

✅ Upload CSV/XLSX files

✅ Store data securely in cloud storage

✅ Generate BCNF schemas with AI

✅ Save normalized results in SQL DB

✅ Dual-cloud support: AWS + GCP

✅ Easy deployment via Streamlit


## 🛠️ Technologies Used

| Category | AWS | GCP |
|-----------|-----|-----|
| **UI / Frontend** | Streamlit (local) | Streamlit (local) |
| **Backend** | Python | Python |
| **AI Engine** | Bedrock (Claude/Sonnet) via AWS Lambda | Gemini AI via API Key |
| **Storage** | Amazon S3 | Google Cloud Storage |
| **Database** | Amazon RDS (MySQL) | Cloud SQL (MySQL) |
| **Compute** | AWS Lambda | Local Execution (app.py) |
| **SDK / Libraries** | boto3, sqlalchemy | google-cloud-storage, google-generativeai |

---

## 🔒 Environment Variables

| Variable | Description |
|-----------|-------------|
| `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` | AWS credentials |
| `RDS_ENDPOINT`, `DB_USER`, `DB_PASS` | RDS connection details |
| `GEMINI_API_KEY` | Gemini AI API key |
| `GOOGLE_APPLICATION_CREDENTIALS` | Path to GCP service account JSON |
| `PROJECT_ID`, `BUCKET_NAME`, `INSTANCE_CONNECTION_NAME` | GCP resource info |


> **Note:**  
> AWS Bedrock access is limited in the free tier. Due to restricted access to certain foundation models and API usage limits, generating and capturing AI normalization results (snapshots) from AWS Bedrock could not be demonstrated fully in this project. However, the Lambda integration and workflow setup remain functional.
