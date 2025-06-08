# 🧠 TalentScout Hiring Assistant

## Project Overview

TalentScout Hiring Assistant is an interactive chatbot built with Streamlit that helps candidates prepare for technical interviews. It collects basic candidate information step-by-step, then generates personalized technical interview questions based on the candidate’s tech stack using OpenRouter’s GPT API. The assistant delivers questions one at a time and allows users to exit anytime by typing commands like “exit” or “bye.” It’s designed to simulate a friendly, paced interview experience in a web app.

## Installation Instructions

Follow these steps to get the Hiring Assistant running on your local machine:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Disha-Sikka/Chatbot
   cd Chatbot
   ```


2. **Install required packages:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key:**
   Create a `.streamlit/secrets.toml` file and add your OpenRouter API key like this:

   ```
   OPENROUTER_API_KEY="your_api_key_here"
   ```

4. **Run the Streamlit app:**

   ```bash
   streamlit run app.py
   ```

5. Your default browser should open the chatbot interface. If it doesn’t, open `http://localhost:8501` manually.

---

## Usage Guide

* The assistant will ask you a series of questions to gather your:

  * Full name
  * Email
  * Phone number
  * Years of experience
  * Desired position
  * Location
  * Tech stack

* After you input your tech stack, it will generate 3 to 5 relevant technical interview questions tailored to your skills.

* Questions appear **one at a time** for you to answer comfortably.

* You can exit the interview at any time by typing commands like `exit`, `bye`, or `quit`.

---

## Technical Details

* **Framework:** Streamlit for interactive UI
* **API Client:** OpenRouter’s Python SDK to interact with GPT-3.5 Turbo
* **Programming Language:** Python 3.8+
* **Model:** GPT-3.5 Turbo (via OpenRouter API) for natural language understanding and question generation
* **Architecture:** Session state manages conversation flow and stores user data to keep track across interactions

---

## Prompt Design

The prompts were carefully crafted to:

* Guide the assistant to collect basic candidate info **step-by-step** to avoid overwhelming the user.
* Generate **concise, relevant technical questions** based on the provided tech stack, focusing on beginner to intermediate difficulty.
* Support user-friendly commands like `exit` and `bye` to gracefully end the session.
* Maintain a conversational tone, keeping the interaction engaging yet professional.

---

## Challenges & Solutions

* **Managing conversation flow:** Handling multi-step inputs while maintaining state was tricky. Solved using Streamlit’s `session_state` to store progress and data seamlessly.
* **API interaction issues:** Initially, API calls failed due to incorrect usage of the OpenAI client. Fixed by switching to OpenRouter’s Python SDK and ensuring proper API key configuration.
* **Generating questions one-by-one:** The original implementation showed all questions at once. Added logic to present questions sequentially, improving user experience.
* **Validating user input:** Ensured email and phone formats were validated using regex to maintain data quality.

---
