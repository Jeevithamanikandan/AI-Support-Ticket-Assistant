import pandas as pd

class DataLoader:

    def __init__(self, path):
        self.path = path
        self.df = None

    def load(self):

        self.df = pd.read_csv(self.path)

        self.df.columns = [
            "ticket_id",
            "created_at",
            "category",
            "priority",
            "status",
            "response_time_hrs",
            "resolution_time_hrs",
            "agent_id",
            "customer_rating",
            "issue_summary"
        ]

        self.df["created_at"] = pd.to_datetime(
        self.df["created_at"],
        format="%d-%m-%Y %H:%M",
        errors="coerce"
    )

        return self.df