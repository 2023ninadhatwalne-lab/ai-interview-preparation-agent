import streamlit as st
from database import init_db, save_session, get_sessions, get_topic_stats
from interview import TOPICS, ROLE_PRESETS, generate_question, evaluate_answer, build_revision
from datetime import datetime

st.set_page_config(page_title="InterviewPrep AI", page_icon="🎯", layout="wide")
init_db()

st.title("🎯 InterviewPrep AI")
st.caption("Your personal technical interview coach — practice, get feedback, and improve.")

with st.sidebar:
    st.header("Interview setup")
    role = st.selectbox("Target role", list(ROLE_PRESETS.keys()))
    level = st.selectbox("Experience level", ["Fresher", "Junior", "Intermediate"], index=0)
    focus = st.multiselect("Topics to practice", TOPICS, default=ROLE_PRESETS[role])
    if not focus:
        focus = ROLE_PRESETS[role]
    st.divider()
    page = st.radio("Navigate", ["Mock interview", "Practice by topic", "Progress dashboard", "Revision plan"])

if page == "Mock interview":
    st.subheader("Mock interview")
    st.write(f"**Role:** {role} · **Level:** {level}")
    if "question" not in st.session_state:
        st.session_state.question = generate_question(role, focus, level)
        st.session_state.answer = ""
        st.session_state.feedback = None
    st.markdown("### Interviewer's question")
    st.info(st.session_state.question["question"])
    st.caption(f"Topic: {st.session_state.question['topic']} · Difficulty: {st.session_state.question['difficulty']}")
    answer = st.text_area("Your answer", key="answer", height=190, placeholder="Explain your approach clearly. Include examples where possible.")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Evaluate my answer", type="primary", use_container_width=True):
            if len(answer.strip()) < 20:
                st.warning("Write at least a few sentences so the evaluator can give useful feedback.")
            else:
                feedback = evaluate_answer(st.session_state.question, answer)
                st.session_state.feedback = feedback
                save_session(role, st.session_state.question["topic"], st.session_state.question["question"], answer, feedback)
    with c2:
        if st.button("Skip / next question", use_container_width=True):
            st.session_state.question = generate_question(role, focus, level)
            st.session_state.answer = ""
            st.session_state.feedback = None
            st.rerun()
    if st.session_state.feedback:
        f = st.session_state.feedback
        st.divider()
        st.subheader("Feedback")
        a,b,c = st.columns(3)
        a.metric("Overall score", f'{f["score"]}/10')
        b.metric("Technical coverage", f'{f["technical"]}/10')
        c.metric("Communication", f'{f["communication"]}/10')
        st.write("**What you did well**")
        for item in f["strengths"]: st.write("• " + item)
        st.write("**What to improve**")
        for item in f["improvements"]: st.write("• " + item)
        st.write("**Suggested model answer structure**")
        st.success(f["model_answer"])

elif page == "Practice by topic":
    st.subheader("Practice by topic")
    topic = st.selectbox("Choose a topic", TOPICS)
    if "practice_q" not in st.session_state or st.session_state.get("practice_topic") != topic:
        st.session_state.practice_q = generate_question(role, [topic], level)
        st.session_state.practice_topic = topic
    st.info(st.session_state.practice_q["question"])
    practice_answer = st.text_area("Your answer", key="practice_answer", height=170)
    if st.button("Check answer", type="primary"):
        if len(practice_answer.strip()) < 20:
            st.warning("Please write a little more before checking.")
        else:
            result = evaluate_answer(st.session_state.practice_q, practice_answer)
            save_session(role, topic, st.session_state.practice_q["question"], practice_answer, result)
            st.metric("Score", f'{result["score"]}/10')
            st.write("**Feedback:** " + " ".join(result["improvements"]))
            st.write("**Try to include:** " + ", ".join(result["keywords"]))

elif page == "Progress dashboard":
    st.subheader("Your progress")
    sessions = get_sessions()
    if not sessions:
        st.info("Complete your first practice answer to see your progress here.")
    else:
        scores = [x["score"] for x in sessions]
        x,y,z = st.columns(3)
        x.metric("Attempts", len(sessions))
        y.metric("Average score", f"{sum(scores)/len(scores):.1f}/10")
        z.metric("Topics practiced", len(set(x["topic"] for x in sessions)))
        st.markdown("### Recent attempts")
        st.dataframe([{"Date":x["created_at"],"Role":x["role"],"Topic":x["topic"],"Score":x["score"]} for x in sessions], use_container_width=True)
        stats = get_topic_stats()
        if stats:
            st.markdown("### Performance by topic")
            st.bar_chart({x["topic"]:x["average"] for x in stats})
            weakest = min(stats, key=lambda x:x["average"])
            st.warning(f"Focus next on **{weakest['topic']}** (average {weakest['average']:.1f}/10).")

else:
    st.subheader("Personalized revision plan")
    stats = get_topic_stats()
    if not stats:
        st.info("Practice a few questions first. Your revision plan will be based on your actual scores.")
    else:
        weak = [x for x in sorted(stats, key=lambda x:x["average"]) if x["average"] < 7]
        if not weak:
            st.success("Great work! Your recorded topic averages are all 7/10 or higher. Keep practicing mixed questions.")
        for item in weak:
            st.markdown(f"### {item['topic']} — {item['average']:.1f}/10")
            for task in build_revision(item["topic"]):
                st.write("☐ " + task)

st.divider()
st.caption("MVP note: feedback is generated by a transparent rubric and keyword coverage. Connect an LLM provider later for richer conversational evaluation.")
