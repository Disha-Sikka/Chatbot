import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Set Streamlit page config
st.set_page_config(page_title="TalentScout Assistant", page_icon="🧠")
st.title("🧠 TalentScout Hiring Assistant")

# Session state initialization
if 'stage' not in st.session_state:
    st.session_state.stage = 'greeting'
if 'responses' not in st.session_state:
    st.session_state.responses = {}

# Stage: Greeting
if st.session_state.stage == 'greeting':
    st.markdown("""
    👋 Hello and welcome to **TalentScout**!

    I’m your virtual hiring assistant here to help with your initial screening.
    I’ll be asking you a few questions to get to know you better and then ask some technical questions based on your tech stack.

    👉 Type **start** to begin or **exit** anytime to leave the conversation.
    """)
    user_input = st.text_input("Type here to continue:", key='start_input')

    if user_input.lower() == 'start':
        st.session_state.stage = 'collect_info'
        st.rerun()
    elif user_input.lower() in ['exit', 'quit', 'bye']:
        st.success("Thank you for visiting TalentScout. Goodbye!")
        st.stop()

# Stage: Candidate Info Collection
elif st.session_state.stage == 'collect_info':
    st.subheader("📋 Candidate Information")
    with st.form("candidate_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        phone = st.text_input("Phone Number")
        experience = st.number_input("Years of Experience", min_value=0, max_value=50, step=1)
        position = st.text_input("Desired Position(s)")
        location = st.text_input("Current Location")
        tech_stack = st.text_area("Tech Stack (e.g. Python, Django, PostgreSQL)")

        submitted = st.form_submit_button("Submit")

    if submitted:
        st.session_state.responses = {
            "name": name,
            "email": email,
            "phone": phone,
            "experience": experience,
            "position": position,
            "location": location,
            "tech_stack": tech_stack
        }
        st.success("✅ Candidate information saved.")
        st.session_state.stage = 'generate_questions'
        st.rerun()

# Stage: Generate GPT-based Questions
elif st.session_state.stage == 'generate_questions':
    st.subheader("🤖 Technical Questions Based on Your Tech Stack")

    tech_stack = st.session_state.responses['tech_stack']
    prompt = f"""
You are a technical interviewer. The candidate has experience with the following tech stack:
{tech_stack}

Generate 3-5 technical interview questions that assess the candidate's proficiency in the listed technologies.
Only return the questions without explanations.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful technical interviewer."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )

        questions = response.choices[0].message.content
        st.markdown("### Here are your technical questions:")
        st.markdown(questions.replace("\n", "\n\n"))
        st.success("✅ This concludes your initial screening. Our team will review and contact you soon.")

        st.button("End Session", on_click=lambda: st.session_state.clear())

    except Exception as e:
        st.error("⚠️ Failed to fetch questions. Please check your API key and internet connection.")
        st.exception(e)
