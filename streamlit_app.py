import streamlit as st
import requests
import re

API_BASE = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Personal Finance AI Platform",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# Styling
# -----------------------------
st.markdown("""
<style>
.main { background-color: #0f172a; }
h1, h2, h3, h4 { color: #f8fafc; }

.stButton>button {
    background: linear-gradient(90deg, #2563eb, #1d4ed8);
    color: white;
    border-radius: 10px;
    padding: 0.4rem 1rem;
    border: none;
}

.stChatMessage {
    border-radius: 12px;
    padding: 10px;
}

.block-container {
    padding-top: 2rem;
}

.loading-box {
    background-color: #1e293b;
    padding: 12px;
    border-radius: 8px;
    color: #cbd5e1;
    font-style: italic;
}
</style>
""", unsafe_allow_html=True)

st.title("📊 Personal Finance AI Platform")
st.caption("Enterprise RAG-powered Learning System")

page = st.sidebar.radio(
    "Navigate",
    ["📑 Table of Contents", "🧮 Formula Explorer", "🎓 AI Tutor Chat"]
)

# =========================================================
# 📑 TABLE OF CONTENTS
# =========================================================
if page == "📑 Table of Contents":

    if "toc_data" not in st.session_state:
        st.session_state.toc_data = None

    st.header("Document Knowledge Structure")

    if st.button("Load Table of Contents"):
        try:
            with st.spinner("Loading structure..."):
                response = requests.get(f"{API_BASE}/toc")
                response.raise_for_status()
                st.session_state.toc_data = response.json()["toc"]
        except Exception as e:
            st.error(f"Error loading TOC: {e}")

    if st.session_state.toc_data:
        st.subheader("Structured Table of Contents")

        # First show raw output for debugging (optional but helpful)
        with st.expander("🔎 Raw TOC Output (Debug View)", expanded=False):
            st.text(st.session_state.toc_data)

        # Render as Markdown (professional formatting)
        st.markdown(st.session_state.toc_data)


# =========================================================
# 🧮 FORMULA EXPLORER
# =========================================================
elif page == "🧮 Formula Explorer":

    if "formula_data" not in st.session_state:
        st.session_state.formula_data = None

    st.header("Financial Formula Explorer")

    if st.button("Fetch Formulae"):
        try:
            with st.spinner("Extracting formulas..."):
                response = requests.get(f"{API_BASE}/formulae")
                response.raise_for_status()
                st.session_state.formula_data = response.json()["formulae"]
        except Exception as e:
            st.error(f"Error fetching formulas: {e}")

    if st.session_state.formula_data:
        st.subheader("Extracted Financial Formulae")

        # Optional debug view
        with st.expander("🔎 Raw Output (Debug)", expanded=False):
            st.text(st.session_state.formula_data)

        # Split into logical formula sections (1 formula per section expected)
        formula_blocks = st.session_state.formula_data.split("\n\n")

        for block in formula_blocks:
            if block.strip():

                st.markdown("---")

                lines = block.split("\n")
                formula_rendered = False

                for line in lines:
                    cleaned = line.strip()

                    # First detected equation line → render as LaTeX
                    if not formula_rendered and "=" in cleaned:
                        try:
                            st.latex(cleaned)
                            formula_rendered = True
                        except:
                            st.markdown(f"`{cleaned}`")
                            formula_rendered = True
                    else:
                        st.markdown(cleaned)
# =========================================================
# 🎓 AI TUTOR CHAT
# =========================================================
elif page == "🎓 AI Tutor Chat":

    st.header("Conversational Finance Tutor")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # -----------------------------
    # Suggested Questions (shown when chat is empty)
    # -----------------------------
    selected_question = None
    if len(st.session_state.chat_history) == 0:
        st.subheader("Recommended Questions to Get Started")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("What is Compound Interest?"):
                selected_question = "What is Compound Interest?"
        
            if st.button("Explain Net Present Value"):
                selected_question = "Explain Net Present Value"

        with col2:
            if st.button("What is Portfolio Diversification?"):
                selected_question = "What is Portfolio Diversification?"

            if st.button("Explain Risk vs Return"):
                selected_question = "Explain Risk vs Return"

    # If a recommended question was clicked → trigger response
    if selected_question:
        user_input = selected_question
    else:
        user_input = st.chat_input("Ask a finance question...")

    if user_input:
        st.session_state.chat_history.append(("user", user_input))

        with st.chat_message("assistant"):
            loading_placeholder = st.empty()
            loading_placeholder.markdown("<div class='loading-box'>Generating response...</div>", unsafe_allow_html=True)

        try:
            response = requests.post(
                f"{API_BASE}/teach",
                json={"topic": user_input}
            )
            response.raise_for_status()
            answer = response.json()["lesson"]

            loading_placeholder.empty()
            st.session_state.chat_history.append(("assistant", answer))

            quiz_prompt = f"Generate 3 quiz questions to test understanding of {user_input}"
            quiz_response = requests.post(
                f"{API_BASE}/teach",
                json={"topic": quiz_prompt}
            )
            quiz_response.raise_for_status()
            quiz_content = quiz_response.json()["lesson"]

            formatted_quiz = "### 🧠 Knowledge Check Quiz\n\n" + quiz_content
            st.session_state.chat_history.append(("assistant", formatted_quiz))

        except Exception as e:
            st.error(f"Error generating response: {e}")

    # -----------------------------
    # Display Chat History
    # -----------------------------
    for role, message in st.session_state.chat_history:
        with st.chat_message(role):
            st.markdown(message)

    # -----------------------------
    # Footer placed ABOVE chat input
    # -----------------------------
    st.markdown("---")
    st.caption("Powered by FastAPI • LangChain • Ollama • Chroma")