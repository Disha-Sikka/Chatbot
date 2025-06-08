import streamlit as st
from openai import OpenAI
import re

# Load your OpenRouter API key from Streamlit secrets
api_key = st.secrets["OPENROUTER_API_KEY"]
client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

# Page setup
st.set_page_config(page_title="TalentScout Assistant", page_icon="🧠", layout="centered")
st.title("🧠 TalentScout Hiring Assistant")

# Initialize session state
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.data = {}
    st.session_state.tech_questions = []
    st.session_state.conversation_over = False
    st.session_state.error_msg = ""
    st.session_state.question_index = 0

# Exit keywords
EXIT_KEYWORDS = ["exit", "bye", "quit", "end"]

# Basic info questions
questions = [
    ("full_name", "What is your full name?"),
    ("email", "What is your email address?"),
    ("phone", "What is your phone number?"),
    ("experience", "How many years of experience do you have?"),
    ("position", "What position are you applying for?"),
    ("location", "Where are you currently located?"),
    ("tech_stack", "Please list your tech stack (e.g., Python, Django, MySQL, etc.)"),
]

# Validation
def validate_input(key, value):
    if key == "email":
        return bool(re.match(r"[^@]+@[^@]+\.[^@]+", value.strip()))
    elif key == "phone":
        return bool(re.match(r"^\+?\d{10,15}$", value.strip()))
    elif key == "full_name":
        return len(value.strip().split()) >= 2
    return True

# Exit logic
if not st.session_state.conversation_over:
    st.markdown("👉 You can type `exit`, `bye`, or `quit` anytime to end the conversation.\n")

    current_step = st.session_state.step

    # Collect basic info
    if current_step < len(questions):
        key, prompt = questions[current_step]
        user_input = st.text_input(prompt, key="input")

        if user_input:
            user_input = user_input.strip()
            if user_input.lower() in EXIT_KEYWORDS:
                st.session_state.conversation_over = True
                st.rerun()
            elif validate_input(key, user_input):
                st.session_state.data[key] = user_input
                st.session_state.step += 1
                st.session_state.error_msg = ""
                st.rerun()
            else:
                st.session_state.error_msg = f"⚠️ Invalid input for {key.replace('_', ' ').title()}."

        if st.session_state.error_msg:
            st.warning(st.session_state.error_msg)

    # Generate tech questions
    elif current_step == len(questions):
        tech_stack = st.session_state.data.get("tech_stack", "")
        with st.spinner("Generating technical questions based on your tech stack..."):
            try:
                response = client.chat.completions.create(
                    model="openai/gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You're an expert technical interviewer."},
                        {"role": "user", "content": f"Generate 3 to 5 technical interview questions for a candidate skilled in: {tech_stack}. Keep them concise and relevant."}
                    ],
                    temperature=0.7
                )
                output = response.choices[0].message.content
                questions_generated = [q.strip("- ").strip() for q in output.strip().split("\n") if q.strip()]
                st.session_state.tech_questions = questions_generated
                st.session_state.step += 1
                st.rerun()
            except Exception as e:
                st.error(f"❌ Failed to generate technical questions: {str(e)}")
                st.stop()

    # Show one question at a time
    elif current_step == len(questions) + 1:
        index = st.session_state.question_index
        questions = st.session_state.tech_questions

        if index < len(questions):
            st.subheader("🧪 Technical Question")
            st.write(f"**Q{index + 1}:** {questions[index]}")
            user_input = st.text_input("Your answer (type 'exit' to end):", key=f"answer_{index}")

            if user_input.lower().strip() in EXIT_KEYWORDS:
                st.session_state.conversation_over = True
                st.rerun()
            elif user_input:
                st.session_state.question_index += 1
                st.rerun()
        else:
            st.session_state.conversation_over = True
            st.rerun()

else:
    st.success("✅ Thank you for your responses! We will review your information and contact you shortly.")
    st.balloons()
