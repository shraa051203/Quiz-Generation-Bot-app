import streamlit as st
from quiz_generator import generate_fill_in_blanks, generate_mcqs
from science2_chapter_texts import science2_chapter_texts
from geography_chapter_texts import geography_chapter_texts
from pdf_utils import export_quiz_to_pdf

# Normalize geography chapter keys
normalized_geography = {
    key.strip().lower(): value for key, value in geography_chapter_texts.items()
}

# Subject → Chapters mapping
subjects = {
    "Science 2": list(science2_chapter_texts.keys()),
    "Geography": list(geography_chapter_texts.keys()),
}

# Page config
st.set_page_config(page_title="🧠 Quiz Generator Bot", layout="wide")
st.title("🧠 Quiz Generator Bot")

# Sidebar Settings
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    quiz_mode = st.radio("Choose Mode", ["Quiz", "Test"])
    use_custom_input = st.checkbox("✍️ Use Custom Input")
    custom_input = ""
    if use_custom_input:
        custom_input = st.text_area("Paste your content here", height=300)
    quiz_types = st.multiselect("Question Types", ["Fill in the Blanks", "Multiple Choice Questions"],
                                default=["Fill in the Blanks", "Multiple Choice Questions"])

# Main Area: Subject & Chapter Selection
selected_subject = st.selectbox("Select Subject", list(subjects.keys()))
selected_chapter = st.selectbox("Select Chapter", subjects[selected_subject])

# Determine which content to use
if use_custom_input and custom_input.strip():
    text_to_use = custom_input.strip()
elif selected_subject == "Science 2":
    text_to_use = science2_chapter_texts.get(selected_chapter, "")
elif selected_subject == "Geography":
    text_to_use = normalized_geography.get(selected_chapter.strip().lower(), "")
else:
    text_to_use = ""

# Generate Quiz/Test
if st.button(f"Generate {quiz_mode}"):
    if not text_to_use:
        st.warning("⚠️ No content found.")
    else:
        with st.spinner("Generating..."):
            st.session_state.blanks = generate_fill_in_blanks(text_to_use) if "Fill in the Blanks" in quiz_types else []
            st.session_state.mcqs = generate_mcqs(text_to_use) if "Multiple Choice Questions" in quiz_types else []
            st.session_state.quiz_mode = quiz_mode.lower()

# --- QUIZ MODE: Show with answers ---
if st.session_state.get("quiz_mode") == "quiz":
    blanks = st.session_state.get("blanks", [])
    mcqs = st.session_state.get("mcqs", [])

    if blanks:
        st.subheader("📝 Fill in the Blanks")
        for i, (q, ans) in enumerate(blanks, 1):
            st.markdown(f"**{i}.** {q}")
            st.markdown(f"<details><summary>Show Answer</summary><i>{ans}</i></details>", unsafe_allow_html=True)

    if mcqs:
        st.subheader("❓ Multiple Choice Questions")
        for i, (q, ans, opts) in enumerate(mcqs, 1):
            st.markdown(f"**{i}.** {q}")
            for label, option in opts.items():
                st.markdown(f"**{label}.** {option}")
            st.markdown(f"<details><summary>Show Answer</summary><i>{ans}</i></details>", unsafe_allow_html=True)

    if st.button("📄 Export as PDF"):
        pdf_path = export_quiz_to_pdf(blanks, mcqs)
        with open(pdf_path, "rb") as f:
            st.download_button("⬇️ Download Quiz PDF", f, file_name="quiz.pdf", mime="application/pdf")

# --- TEST MODE: Interactive + Scoring ---
elif st.session_state.get("quiz_mode") == "test":
    blanks = st.session_state.get("blanks", [])
    mcqs = st.session_state.get("mcqs", [])
    user_answers = {}
    total_questions = len(blanks) + len(mcqs)

    with st.form("quiz_form"):
        st.subheader("🧪 Take the Test")

        # Fill in the blanks
        for i, (q, ans) in enumerate(blanks, 1):
            user_input = st.text_input(f"{i}. {q}", key=f"blank_{i}")
            user_answers[f"blank_{i}"] = (q, ans.strip(), user_input.strip())

        # MCQs
        offset = len(blanks)
        for j, (q, correct_ans, options) in enumerate(mcqs, offset + 1):
            user_choice = st.radio(f"{j}. {q}", options=list(options.values()), key=f"mcq_{j}")
            user_answers[f"mcq_{j}"] = (q, options.get(correct_ans, "").strip(), user_choice.strip(), options)

        submitted = st.form_submit_button("📝 Submit Test")

    if submitted:
        score = 0
        evaluated_blanks = []
        evaluated_mcqs = []

        st.subheader("📊 Results")
        for key, data in user_answers.items():
            if key.startswith("blank_"):
                q, correct, user = data
                evaluated_blanks.append((q, correct, user))
                if user.lower() == correct.lower():
                    st.success(f"✅ {q} — Correct")
                    score += 1
                else:
                    st.error(f"❌ {q} — Your Answer: `{user}` | Correct: `{correct}`")
            elif key.startswith("mcq_"):
                q, correct, user, opts = data
                evaluated_mcqs.append((q, correct, opts, user))
                if user.lower() == correct.lower():
                    st.success(f"✅ {q} — Correct")
                    score += 1
                else:
                    st.error(f"❌ {q} — Your Answer: `{user}` | Correct: `{correct}`")

        st.markdown(f"### 🏁 Final Score: **{score} / {total_questions}**")

        if st.button("📄 Export Test as PDF"):
            pdf_path = export_quiz_to_pdf(evaluated_blanks, evaluated_mcqs, score=score, total=total_questions)
            with open(pdf_path, "rb") as f:
                st.download_button("⬇️ Download Test PDF", f, file_name="test_result.pdf", mime="application/pdf")

        if st.button("🔁 Try Again"):
            st.session_state.clear()
