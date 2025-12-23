import sqlite3
import pandas as pd
import numpy as np


connection = sqlite3.connect("app_database.db")

df = pd.read_sql_query("SELECT timestamp, event_tpes, app_name, duration, key_count, mouse_count, extra FROM users", connection)

connection.close()

df["timestamp"] = pd.to_datetime(df["timestamp"], unit= 's')
df = df.sort_values("timestamp")

WINDOW = "5min"

df["window_start"] = df["timestamp"].dt.floor(WINDOW)


grouped = df.groupby("window_start")

features = grouped.agg(
    total_keys =("key_count", "sum"),
    total_mouse =("mouse_count", "sum"),
    total_duration =("duration", "sum"),
    idle_time =("event_tpes", lambda x: (x == "idle").sum() * 10),
    
)

features["active_time"] = features['total_duration'] - features["idle_time"]

features["typing_rate"] = features["total_keys"]/ features["total_duration"]


features["interaction_intensity"] = (features["total_keys"] + features["total_mouse"]) / features["total_duration"]

def app_switching(app_series):
    return(app_series != app_series.shift()).sum() - 1

features["app_switches"] = grouped["app_name"].apply(app_switching)

features["dominant_app"] = grouped["app_name"].agg(
    lambda x: x.value_counts().idxmax()
)

features = features.reset_index()

print(features.head())

features.to_csv("features.csv", index=False)
print("Saved features.csv")


