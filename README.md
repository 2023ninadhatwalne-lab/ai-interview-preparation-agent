# InterviewPrep AI — AI Interview Preparation Agent

A practical interview-preparation dashboard for freshers and junior developers. Select a target role, practice technical questions, receive structured feedback, track topic-wise scores, and get a revision plan.

## Features
- Role-based question selection for Python, SQL, ML, NLP, RAG, APIs, Cloud/DevOps, System Design, DSA, and OOP/Java.
- Mock interview and topic-wise practice modes.
- Rubric-based scoring for technical coverage and communication.
- Strengths, improvement suggestions, and answer-structure guidance.
- SQLite history, progress dashboard, and weak-topic revision plan.

## Tech stack
- Python 3.10+
- Streamlit
- SQLite

## Run locally (Windows PowerShell)
```powershell
cd ai-interview-preparation-agent
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```
Open the local URL printed by Streamlit (usually http://localhost:8501).

## Project structure
```text
ai-interview-preparation-agent/
├── app.py
├── interview.py
├── database.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Evaluation approach
The current MVP uses a transparent keyword-coverage rubric plus answer-length/structure signals. It is deterministic enough for a demo and does not require a paid API key. It is **not** a substitute for expert human evaluation. For production use, connect an LLM evaluator with JSON-schema output, add authentication, and deploy the app with managed database storage.

## Roadmap
- LLM-powered follow-up questions and semantic evaluation.
- Resume/job-description ingestion and question personalization.
- User accounts and cloud database.
- Speech-to-text mock interviews and communication analytics.
- Exportable performance reports.

## Privacy
Practice answers are stored locally in `interview_prep.db` on the machine running the app. Do not enter confidential personal information.
