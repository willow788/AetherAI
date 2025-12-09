WellnessTracker

A lightweight, fully software-based personal wellness and behavior monitoring system.
Designed to track computer usage patterns such as active applications, typing frequency, mouse activity, and idle durations. The collected data is processed to generate wellness indicators like focus score, burnout risk, productivity rhythm, and daily behavioral trends.

This project runs locally, stores all data on-device, and requires no hardware sensors.

Features

Active Window Tracking
Detects which application is currently in use.

Keyboard & Mouse Activity Monitoring
Counts keystrokes and mouse clicks in real-time.

Idle Detection
Identifies periods of user inactivity.

Lightweight Logging Engine
Records events every 10 seconds in a local SQLite database.

Privacy-Friendly
All data remains offline. No cloud sync, no external APIs.

Model-Ready Dataset
Collected data can be exported or processed for ML tasks such as:

focus/flow detection

distraction measurement

anomaly detection

stress & wellness pattern learning

Project Structure
wellness_tracker/
│
├── collector.py          # Main data capture loop (keyboard, mouse, active window)
├── active_window.py      # Handles active window title extraction
├── database.py           # SQLite initialization and helper
├── check_db.py           # Utility script for verifying logged data
│
├── wellness.db           # Generated after first run
└── README.md             # You are here

Setup
1. Create & activate virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

2. Install dependencies
pip install psutil pynput pywinctl schedule pandas sqlalchemy

Usage
Initialize Database
python database.py

Start Data Collection
python collector.py

Verify Data
python check_db.py

How It Works

The collector runs a 10-second interval loop:

Fetch active window.

Capture keypress & mouse click counts.

Detect idle periods.

Log everything into a normalized SQLite table.

The event table contains:

timestamp

event type

active application

duration

keyboard count

mouse count

optional metadata

This structure is optimized for building classical ML models (SVM, logistic regression), sequence models (RNN/LSTM), or anomaly detectors.

Roadmap

Add app category normalization (Work / Social / Entertainment / Dev).

Implement idle-event logging.

Feature extraction pipeline.

Baseline ML models (focus prediction, distraction score).

Local desktop dashboard (Tkinter / PyQt / Electron).
