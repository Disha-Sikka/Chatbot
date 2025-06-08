import streamlit as st
from openai import OpenAI


api_key = st.secrets["OPENROUTER_API_KEY"]
client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

st.set_page_config(page_title="TalentScout Hiring Assistant", page_icon="🧠", layout="centered")
st.title("🧠 TalentScout Hiring Assistant")

if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.user_data = {}
    st.session_state.tech_questions = []
    st.session_state.tech_answers = {}
    st.session_state.conversation_over = False

questions = [
    ("full_name", "What is your full name?"),
    ("email", "What is your email address?"),
    ("phone", "What is your phone number?"),
    ("experience", "How many years of experience do you have?"),
    ("position", "What position are you applying for?"),
    ("location", "Where are you currently located?"),
    ("tech_stack", "Please list your tech stack (e.g., Python, Django, MySQL, etc.)"),
]


if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "assistant", "content": "Hello! I'm the TalentScout Hiring Assistant. Let's get started with a few questions."})
    st.session_state.messages.append({"role": "assistant", "content": questions[0][1]})

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

def generate_questions(tech_stack):
    prompt = f"""You are a technical interviewer. Generate 3-5 concise technical interview questions for each of the following tech stack items provided by a candidate:\n\nTech Stack: {tech_stack}\n\nKeep questions relevant and beginner-to-intermediate level."""

    try:
        response = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        questions = response.choices[0].message.content.strip().split("\n")
        st.session_state.tech_questions = [q.strip("•-1234567890. ") for q in questions if q.strip()]
        st.session_state.step += 1  # Proceed to question asking phase
        first_question = st.session_state.tech_questions[0]
        st.session_state.messages.append({"role": "assistant", "content": f"Here is your first technical question:\n\n{first_question}"})
    except Exception as e:
        st.session_state.messages.append({"role": "assistant", "content": f"Error generating questions: {e}"})
        st.session_state.conversation_over = True


def handle_input(user_input):
    st.session_state.messages.append({"role": "user", "content": user_input})

    if user_input.lower() in ["exit", "quit", "bye", "done", "thank you"]:
        st.session_state.messages.append({"role": "assistant", "content": "✅ Thank you for your time! We’ll review your responses and get back to you. Have a great day!"})
        st.session_state.conversation_over = True
        return

    step = st.session_state.step


    if step < len(questions):
        key, _ = questions[step]
        st.session_state.user_data[key] = user_input
        st.session_state.step += 1

        if st.session_state.step < len(questions):
            next_q = questions[st.session_state.step][1]
            st.session_state.messages.append({"role": "assistant", "content": next_q})
        else:
            st.session_state.messages.append({"role": "assistant", "content": "Thanks! Now generating technical questions..."})
            generate_questions(st.session_state.user_data.get("tech_stack", ""))

    else:
        q_index = len(st.session_state.tech_answers)
        st.session_state.tech_answers[q_index] = user_input

        if q_index + 1 < len(st.session_state.tech_questions):
            next_q = st.session_state.tech_questions[q_index + 1]
            st.session_state.messages.append({"role": "assistant", "content": next_q})
        else:
            st.session_state.messages.append({"role": "assistant", "content": "✅ You've completed all technical questions! Type `exit` to finish."})
            st.session_state.conversation_over = True


if not st.session_state.conversation_over:
    if prompt := st.chat_input("Type your answer here..."):
        handle_input(prompt)
        st.rerun()
else:
    st.success("🎉 Interview complete! Thank you for your responses.")
    st.balloons()
