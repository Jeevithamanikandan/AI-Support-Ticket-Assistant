# ui/app.py

import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="AI Support Assistant",
    layout="wide"
)

st.title("🤖 AI Support Ticket Assistant")
try:
    health = requests.get(f"{API_URL}/health").json()

    st.success("🟢 API Connected")

except:

    st.error("🔴 Backend Not Running")

    st.stop()

menu = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Ask AI",
        "Anomaly Detection"
    ]
)

# ===========================================
# Dashboard
# ===========================================

if menu == "Dashboard":

    st.header("Dashboard")

    data = requests.get(f"{API_URL}/dashboard").json()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Tickets", data["total_tickets"])
    c2.metric("Open", data["open_tickets"])
    c3.metric("Resolved", data["resolved_tickets"])
    c4.metric("Escalated", data["escalated_tickets"])

    st.divider()

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Avg Response Time",
        data["average_response_time"]
    )

    c2.metric(
        "Avg Resolution Time",
        data["average_resolution_time"]
    )

    c3.metric(
        "Avg Customer Rating",
        data["average_customer_rating"]
    )

# ===========================================
# Ask AI
# ===========================================

elif menu == "Ask AI":

    st.header("Ask Questions")

    question = st.text_input(
        "Enter your question"
    )

    if st.button("Ask AI"):

        if not question.strip():
            st.warning("Please enter a question before asking AI.")
        else:
            response = requests.post(

                f"{API_URL}/query",

                json={
                    "question": question
                }

            ).json()

            st.subheader("Answer")

            if response.get("success"):

                st.success(response.get("answer", ""))

                with st.expander("View Generated Pandas Code"):

                    st.code(response.get("generated_code", ""))

                    st.subheader("Raw Result")

                    st.write(response.get("result", ""))

            else:

                st.error(response.get("error", "Unable to process your request."))

# ===========================================
# Anomalies
# ===========================================

elif menu == "Anomaly Detection":

    st.header("Detected Anomalies")

    response = requests.get(
        f"{API_URL}/anomalies"
    ).json()

    st.metric(
        "Total Anomalies",
        response["total_anomalies"]
    )

    if response["total_anomalies"] == 0:

        st.success("No anomalies found")

    else:

        df = pd.DataFrame(
            response["anomalies"]
        )

        st.dataframe(
            df,
            use_container_width=True
        )

        if "type" in df.columns:

            fig = px.histogram(
                df,
                x="type",
                title="Anomaly Distribution"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )