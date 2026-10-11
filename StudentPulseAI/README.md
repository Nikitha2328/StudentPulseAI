# StudentPulse AI

**AI-Powered Student Success & Early-Warning Dashboard**  
*Every Student Matters. Every Insight Counts.*

StudentPulse AI is a hackathon MVP that turns student attendance, marks, and assignment-completion data into transparent early-warning indicators and practical support suggestions.

## Features
- Dashboard KPIs for student count, average attendance, average marks, and high-risk flags
- Charts for attendance, marks, assignment completion, and risk distribution
- Search and risk-level filters
- Explainable, rule-based risk score
- Personalized next-step suggestions based on the indicators
- CSV-based data source

## Run locally
```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Deploy on Streamlit Community Cloud
1. Upload `app.py`, `requirements.txt`, and `student_data.csv` to a GitHub repository.
2. In Streamlit Community Cloud, create a new app from that repository.
3. Select `app.py` as the main file and deploy.

## Data and responsible use
The included dataset is synthetic and intended only for demonstration. Risk flags are simple rule-based indicators, not outputs from a trained AI model and not definitive judgments about students. Use authorized, anonymized data and human review before real-world use.
