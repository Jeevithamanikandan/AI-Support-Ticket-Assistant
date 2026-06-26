# app/query_engine.py

import pandas as pd
import numpy as np
from llm_service import GeminiService


class QueryEngine:

    def __init__(self, dataframe):
        self.df = dataframe
        self.llm = GeminiService()

    def execute(self, question):

        code = self.llm.generate_code(question)

        safe_globals = {
            "__builtins__": {
                "len": len,
                "sum": sum,
                "min": min,
                "max": max,
                "round": round,
                "sorted": sorted,
                "list": list
            },
            "pd": pd,
            "np": np
        }

        safe_locals = {
            "df": self.df
        }

        try:

            result = eval(code, safe_globals, safe_locals)

            if isinstance(result, pd.DataFrame):
                result = result.to_dict(orient="records")

            elif isinstance(result, pd.Series):
                result = result.to_dict()

            elif hasattr(result, "item"):
                result = result.item()

            answer = self.llm.format_answer(question, result)

            return {
                "success": True,
                "question": question,
                "generated_code": code,
                "result": result,
                "answer": answer
            }

        except Exception as e:

            return {
                "success": False,
                "question": question,
                "generated_code": code,
                "error": str(e)
            }