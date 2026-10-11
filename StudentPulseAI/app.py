import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="StudentPulse AI",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
.block-container {padding-top: 1.6rem; padding-bottom: 2rem;}
[data-testid="stMetric"] {
    background: rgba(120, 120, 120, 0.08);
    border: 1px solid rgba(120, 120, 120, 0.18);
    padding: 16px 18px;
    border-radius: 14px;
}
.pulse-subtitle {font-size: 1.05rem; opacity: .78;}
</style>
""", unsafe_allow_html=True)

st.title("📈 StudentPulse AI")
st.markdown('<div class="pulse-subtitle">AI-powered student success & early-warning dashboard</div>', unsafe_allow_html=True)
st.caption("Every Student Matters. Every Insight Counts.")

DATA_PATH = Path(__file__).parent / "student_data.csv"

@st.cache_data
def load_data():
    if DATA_PATH.exists():
        df = pd.read_csv(DATA_PATH)
    else:
        df = pd.DataFrame({
            "student_id": [f"S{i:03d}" for i in range(1, 11)],
            "student_name": ["Aarav", "Diya", "Rahul", "Priya", "Arjun", "Meera", "Kiran", "Anaya", "Rohan", "Sana"],
            "attendance_pct": [92, 65, 78, 45, 88, 72, 58, 96, 81, 69],
            "marks_pct": [85, 48, 62, 35, 91, 55, 42, 89, 74, 51],
            "assignments_pct": [90, 55, 70, 40, 95, 65, 50, 92, 80, 60],
        })
    required = {"student_id", "student_name", "attendance_pct", "marks_pct", "assignments_pct"}
    missing = required - set(df.columns)
    if missing:
        st.error("Dataset is missing required columns: " + ", ".join(sorted(missing)))
        st.stop()
    for col in ["attendance_pct", "marks_pct", "assignments_pct"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).clip(0, 100)
    return df

df = load_data()
df["risk_score"] = (
    (100 - df["attendance_pct"]) * 0.40
    + (100 - df["marks_pct"]) * 0.40
    + (100 - df["assignments_pct"]) * 0.20
).round(1)

def risk_label(score):
    if score >= 55:
        return "High"
    if score >= 35:
        return "Medium"
    return "Low"

df["risk_level"] = df["risk_score"].apply(risk_label)

with st.sidebar:
    st.header("🔎 Explore students")
    search = st.text_input("Search by student name or ID")
    risk_filter = st.multiselect("Risk level", ["High", "Medium", "Low"], default=["High", "Medium", "Low"])
    st.divider()
    st.caption("Demo uses synthetic sample data. Replace it with authorized, anonymized data for real use.")

view = df[df["risk_level"].isin(risk_filter)].copy()
if search.strip():
    view = view[
        view["student_name"].str.contains(search.strip(), case=False, na=False)
        | view["student_id"].str.contains(search.strip(), case=False, na=False)
    ]

total = len(df)
high_count = int((df["risk_level"] == "High").sum())
medium_count = int((df["risk_level"] == "Medium").sum())
avg_attendance = df["attendance_pct"].mean()
avg_marks = df["marks_pct"].mean()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Students tracked", total)
c2.metric("High-risk flags", high_count, help="Rule-based indicator, not a diagnosis or final decision")
c3.metric("Average attendance", f"{avg_attendance:.1f}%")
c4.metric("Average marks", f"{avg_marks:.1f}%")

st.subheader("📊 Student performance overview")
left, right = st.columns([1.2, 1])
with left:
    chart_df = df.set_index("student_name")[["attendance_pct", "marks_pct", "assignments_pct"]]
    st.bar_chart(chart_df, y_label="Percentage")
with right:
    risk_counts = df["risk_level"].value_counts().reindex(["High", "Medium", "Low"], fill_value=0)
    st.markdown("**Risk distribution**")
    st.bar_chart(risk_counts)
    st.info("Risk levels are transparent rule-based estimates from attendance, marks, and assignment completion.")

st.subheader("🚦 Early-warning student list")
display = view[["student_id", "student_name", "attendance_pct", "marks_pct", "assignments_pct", "risk_score", "risk_level"]].copy()
display.columns = ["Student ID", "Student", "Attendance %", "Marks %", "Assignments %", "Risk score", "Risk level"]
st.dataframe(display, use_container_width=True, hide_index=True)

st.subheader("🧭 Suggested next steps")
if view.empty:
    st.write("No students match the current filters.")
else:
    for _, row in view.sort_values("risk_score", ascending=False).head(8).iterrows():
        with st.expander(f"{row['student_name']} · {row['risk_level']} risk · score {row['risk_score']:.1f}"):
            actions = []
            if row["attendance_pct"] < 75:
                actions.append("Meet the student to understand attendance barriers and agree on a realistic attendance goal.")
            if row["marks_pct"] < 50:
                actions.append("Create a short revision plan focused on two weak topics and schedule a check-in.")
            elif row["marks_pct"] < 65:
                actions.append("Provide targeted practice questions and review progress after one week.")
            if row["assignments_pct"] < 60:
                actions.append("Break pending assignments into smaller tasks with clear due dates.")
            if not actions:
                actions.append("Continue regular check-ins and encourage consistent study habits.")
            for action in actions:
                st.write("• " + action)

st.caption("Prototype notice: This dashboard uses synthetic demo data and explainable thresholds. It does not use a trained predictive model. Educators should verify context before acting on any risk flag.")
