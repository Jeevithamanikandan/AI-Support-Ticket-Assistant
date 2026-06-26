# app/anomaly_detector.py

from datetime import datetime
import pandas as pd


class AnomalyDetector:

    def __init__(self, df):
        self.df = df.copy()
        self.df["created_at"] = pd.to_datetime(self.df["created_at"])

    def detect(self):

        anomalies = []

        now = datetime.now()

        # ----------------------------
        # 1. Critical tickets older than 24 hrs
        # ----------------------------
        critical = self.df[
            (self.df["priority"] == "Critical") &
            (self.df["status"] != "Resolved")
        ]

        for _, row in critical.iterrows():

            age = (now - row["created_at"]).total_seconds() / 3600

            if age > 24:
                anomalies.append({
                    "type": "Critical Ticket Older Than 24 Hours",
                    "ticket_id": row["ticket_id"],
                    "priority": row["priority"],
                    "status": row["status"],
                    "hours_open": round(age, 2)
                })

        # ----------------------------
        # 2. Long Resolution Time
        # ----------------------------
        avg_resolution = self.df["resolution_time_hrs"].mean()

        threshold = avg_resolution * 2

        long_resolution = self.df[
            self.df["resolution_time_hrs"] > threshold
        ]

        for _, row in long_resolution.iterrows():

            anomalies.append({
                "type": "Abnormally Long Resolution Time",
                "ticket_id": row["ticket_id"],
                "resolution_time": row["resolution_time_hrs"]
            })

        # ----------------------------
        # 3. Slow First Response
        # ----------------------------
        avg_response = self.df["response_time_hrs"].mean()

        threshold = avg_response * 2

        slow_response = self.df[
            self.df["response_time_hrs"] > threshold
        ]

        for _, row in slow_response.iterrows():

            anomalies.append({
                "type": "Slow First Response",
                "ticket_id": row["ticket_id"],
                "response_time": row["response_time_hrs"]
            })

        # ----------------------------
        # 4. Missing Customer Rating
        # ----------------------------
        missing_rating = self.df[
            (self.df["status"] == "Resolved") &
            (self.df["customer_rating"].isna())
        ]

        for _, row in missing_rating.iterrows():

            anomalies.append({
                "type": "Missing Customer Rating",
                "ticket_id": row["ticket_id"]
            })

        return anomalies