# ============================================================
#  ui.py  —  Streamlit UI
#  Run with:  streamlit run ui.py
# ============================================================

import sys, os
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'sections'))

import streamlit as st
from data_loader import load_data, get_summary

import section1_performance as s1
import section2_training     as s2
import section3_behavior     as s3
import section4_projects     as s4
import section5_attrition    as s5
import section6_compensation as s6
import section7_recruitment  as s7

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title = "Employee Analytics AI",
    page_icon  = "🧠",
    layout     = "wide",
)

# ── Custom CSS ───────────────────────────────────────────────
st.markdown("""
<style>
  .main { background: #0f0f1a; }
  .stApp { background: #0f0f1a; }
  h1 { color: #7c6af7 !important; }
  h2 { color: #f7a26a !important; }
  h3 { color: #6af7c4 !important; }
  .stButton>button {
    background: linear-gradient(135deg, #7c6af7, #9f8ffa);
    color: white; border: none; border-radius: 8px;
    padding: 8px 20px; font-weight: 600;
  }
  .stButton>button:hover { opacity: 0.85; }
  .answer-box {
    background: #1a1a2e; border: 1px solid #2a2a4a;
    border-radius: 12px; padding: 20px; margin-top: 12px;
    color: #e0e0f0; font-size: 15px; line-height: 1.7;
  }
  .data-box {
    background: #111120; border: 1px solid #1e1e3a;
    border-radius: 8px; padding: 12px; margin-top: 8px;
    font-family: monospace; font-size: 12px; color: #888aaa;
  }
</style>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────────
st.title("🧠 Employee Analytics Intelligence")
st.caption("GenAI Use Case — Quantiphi | Powered by Claude AI")

# ── Dataset summary ──────────────────────────────────────────
with st.expander("📊 Dataset Overview", expanded=False):
    df = load_data()
    st.code(get_summary(df))
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Employees", "4,000")
    col2.metric("Total Columns",   "109")
    col3.metric("Resigned",        "2,001 (50%)")
    col4.metric("Avg Performance", "9.91")

st.divider()

# ── Section config ───────────────────────────────────────────
SECTIONS = {
    "🔍 Section 1 — Performance & Skills":    (s1, ["Weighted Skill Model", "High Perf + Low Leadership", "High vs Low Performers", "Skill-Outcome Inconsistencies", "Ideal Employee Profile"]),
    "📊 Section 2 — Training & Mentorship":   (s2, ["Dev Hours vs Performance", "Mentor Impact on Conversion", "Training but Low Performance", "Basic vs Advanced Training", "Who Benefits from Advanced Training"]),
    "🧠 Section 3 — Behavioral Intelligence": (s3, ["Soft Skills Clustering", "Conflict vs Teamwork Contradiction", "Engagement vs Retention", "High Initiative, Low Innovation"]),
    "💼 Section 4 — Project Performance":     (s4, ["Complexity vs Outcome", "Successful vs Failed Patterns", "Predictive Success Model", "Role-based Performance"]),
    "📉 Section 5 — Attrition & Retention":   (s5, ["Resignation Factors", "At-Risk Employee Profile", "WLB vs Overtime vs Engagement"]),
    "💰 Section 6 — Compensation":            (s6, ["Salary vs Performance", "Underpaid Employees", "Benefits vs Retention"]),
    "🎯 Section 7 — Recruitment":             (s7, ["Hiring Source Impact", "Best Long-Term Source", "Recruitment Optimization"]),
}

# ── Section selector ─────────────────────────────────────────
selected_section = st.selectbox("Choose a Section", list(SECTIONS.keys()))
module, question_labels = SECTIONS[selected_section]

st.subheader(selected_section)

# ── Question selector ────────────────────────────────────────
selected_q_label = st.selectbox("Choose a Question", question_labels)
q_index = question_labels.index(selected_q_label)

# ── Run button ───────────────────────────────────────────────
col_btn, col_all = st.columns([1, 5])

with col_btn:
    run_one = st.button("▶ Analyze")

# ── Single question ──────────────────────────────────────────
if run_one:
    with st.spinner("Claude is analyzing the data..."):
        try:
            question, data_ctx, answer = module.run(q_index)

            st.markdown(f"**❓ Question:** {question}")

            with st.expander("📂 Data Context sent to Claude", expanded=False):
                st.markdown(f'<div class="data-box">{data_ctx}</div>',
                            unsafe_allow_html=True)

            st.markdown("**🤖 Claude's Answer:**")
            st.markdown(f'<div class="answer-box">{answer}</div>',
                        unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error: {e}")
            st.info("Make sure your API key is set correctly in config.py")

st.divider()

# ── Run ALL questions in section ─────────────────────────────
if st.button("⚡ Run ALL Questions in This Section"):
    for i, label in enumerate(question_labels):
        with st.spinner(f"Analyzing: {label}..."):
            try:
                question, data_ctx, answer = module.run(i)
                st.markdown(f"### Q{i+1}: {label}")
                st.markdown(f"**❓** {question}")
                with st.expander("📂 Data Context", expanded=False):
                    st.markdown(f'<div class="data-box">{data_ctx}</div>',
                                unsafe_allow_html=True)
                st.markdown(f'<div class="answer-box">{answer}</div>',
                            unsafe_allow_html=True)
                st.divider()
            except Exception as e:
                st.error(f"Q{i+1} Error: {e}")
