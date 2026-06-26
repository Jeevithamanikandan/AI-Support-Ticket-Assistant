# app/main.py

from fastapi import FastAPI
from models import QueryRequest
from config import CSV_PATH
from data_loader import DataLoader
from query_engine import QueryEngine
from anomaly_detector import AnomalyDetector

app = FastAPI(
    title="AI Support Assistant",
    version="1.0"
)

# -------------------------
# Load Data
# -------------------------
loader = DataLoader(CSV_PATH)
df = loader.load()

engine = QueryEngine(df)
anomaly = AnomalyDetector(df)

# -------------------------
# Home
# -------------------------
@app.get("/")
def home():
    return {
        "message": "AI Support Assistant API Running"
    }

# -------------------------
# Health Check
# -------------------------
@app.get("/health")
def health():
    return {
        "status": "Healthy"
    }

# -------------------------
# Natural Language Query
# -------------------------
@app.post("/query")
def ask_ai(request: QueryRequest):

    result = engine.execute(request.question)

    return result

# -------------------------
# Detect Anomalies
# -------------------------
@app.get("/anomalies")
def get_anomalies():

    data = anomaly.detect()

    return {
        "total_anomalies": len(data),
        "anomalies": data
    }

# -------------------------
# Dashboard Statistics
# -------------------------
@app.get("/dashboard")
def dashboard():

    return {

        "total_tickets": len(df),

        "open_tickets":
        int((df["status"] == "Open").sum()),

        "resolved_tickets":
        int((df["status"] == "Resolved").sum()),

        "escalated_tickets":
        int((df["status"] == "Escalated").sum()),

        "average_response_time":
        round(df["response_time_hrs"].mean(), 2),

        "average_resolution_time":
        round(df["resolution_time_hrs"].mean(), 2),

        "average_customer_rating":
        round(df["customer_rating"].mean(), 2)

    }