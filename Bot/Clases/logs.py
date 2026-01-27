import os
import datetime

class Logs:
    def __init__(self):
        try:
            self.logs = open(os.path.join(os.getcwd(), "logs", f"log-{datetime.datetime.now().date()}.log"), "a", encoding="utf-8")
        except FileNotFoundError:
            os.makedirs(os.path.join(os.getcwd(), "logs"), exist_ok=True)
            self.logs = open(os.path.join(os.getcwd(), "logs", f"log-{datetime.datetime.now().date()}.log"), "a", encoding="utf-8")
        

    def add_log(self, log: str, level: str = "INFO"):
        levels = {
            "DEBUG": 10,
            "INFO": 20,
            "WARNING": 30,
            "ERROR": 40,
            "CRITICAL": 50
        }

        if level not in levels:
            raise ValueError(f"Invalid log level: {level}")

        timestamp = f"[{datetime.datetime.now()}]"
        level = f"[{level.upper()}]"
        self.logs.write(f"[{timestamp}] - {level}: {log}\n")

    def get_logs(self) -> list[str]:
        self.logs.seek(0)
        return self.logs.readlines()

    def close(self):
        self.logs.close()

    def clear_logs(self):
        self.logs.truncate(0)