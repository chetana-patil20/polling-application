# Polling Application

A small polling web app built with Flask, pandas, Jinja2 templates, and CSV storage.

## Features
- View all polls
- Create a poll with one question and three options
- Vote for an option and see vote counts
- Store poll data in `polls.csv`, created automatically on first run
- Basic per-browser cookie check to discourage repeat votes

> The cookie check is only a basic deterrent. Users can clear cookies or use another browser; it is not secure identity-based voting.

## Run locally (Windows PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000

On macOS/Linux, activate with `source .venv/bin/activate`.

Poll data is saved in `polls.csv`, generated automatically and excluded from Git.
