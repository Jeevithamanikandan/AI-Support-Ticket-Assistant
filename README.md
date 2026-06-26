# AI Support Ticket Assistant

## AI Engineer Technical Assessment – DOTMappers

---

# Project Overview

This project is an AI-powered customer support analytics system built using Python, FastAPI, Streamlit, and Google's Gemini API.

The application allows users to ask natural language questions about customer support tickets, detects anomalies in ticket data, and provides a simple dashboard for analytics.

---

# Features

### ✅ Natural Language Querying

Users can ask questions such as:

- How many tickets are currently open?
- Which agent resolved the most tickets?
- Average customer rating for Technical tickets
- Highest resolution time
- Lowest customer rating
- How many Billing tickets are open?

The system converts the question into a Pandas query using Gemini and executes it on the dataset.

---

### ✅ AI Powered Analytics

The application uses Google's Gemini LLM to:

- Understand user intent
- Generate Pandas expressions
- Produce natural language responses

---

### ✅ Anomaly Detection

The system detects:

- Critical tickets older than 24 hours
- Abnormally high resolution times
- Slow response times
- Missing customer ratings for resolved tickets

---

### ✅ Dashboard

Dashboard displays:

- Total Tickets
- Open Tickets
- Resolved Tickets
- Escalated Tickets
- Average Response Time
- Average Resolution Time
- Average Customer Rating

---

### ✅ REST API

Available APIs

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | / | Home |
| GET | /health | Health Check |
| POST | /query | Ask AI Questions |
| GET | /dashboard | Dashboard Statistics |
| GET | /anomalies | Detect Anomalies |

---

# Project Structure

```
AI_Support_Assistant/

│
├── app/
│   ├── main.py
│   ├── config.py
│   ├── data_loader.py
│   ├── llm_service.py
│   ├── query_engine.py
│   ├── anomaly_detector.py
│   └── models.py
│
├── data/
│   └── support_tickets.csv
│
├── ui/
│   └── app.py
│
├── .env
├── requirements.txt
└── README.md
```

---

# Technologies Used

- Python
- FastAPI
- Streamlit
- Pandas
- Plotly
- Google Gemini API
- NumPy
- Pydantic

---

# Installation

## Clone Repository

```bash
git clone <repository_url>

cd AI_Support_Assistant
```

---

## Create Virtual Environment

```bash
conda create -n test python=3.12

conda activate test
```

---

## Install Packages

```bash
pip install -r requirements.txt
```

---

# Environment Variable

Create a `.env` file

```
GEMINI_API_KEY=YOUR_API_KEY
```

---

# Run FastAPI

```bash
cd app

uvicorn main:app --reload
```

Swagger UI

```
http://127.0.0.1:8000/docs
```

---

# Run Streamlit

```bash
cd ui

streamlit run app.py
```

Open

```
http://localhost:8501
```

---

# Sample Questions

```
How many tickets are currently open?

Average customer rating for Technical category

Highest resolution time

Lowest customer rating

Which agent resolved the most tickets?

How many Billing tickets are open?
```

---

# Architecture

```
                User

                  │

                  ▼

            Streamlit UI

                  │

                  ▼

             FastAPI API

                  │

                  ▼

         Gemini LLM Engine

                  │

                  ▼

        Generates Pandas Code

                  │

                  ▼

          Pandas DataFrame

                  │

                  ▼

         Support Ticket CSV
```

---
