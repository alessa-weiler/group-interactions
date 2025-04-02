import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("Group Interactions")
st.write(
    "This is a simple app that uses OpenAI's GPT-3.5 model to simulate group dynamics. "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
    "First, there is some onboarding information, and then you can enter the names and texts of the people in your group. "
    "The app will then generate an analysis of group dynamics."
)
number_of_people = st.number_input(
    "Number of people in the group",
    min_value=1,
    max_value=10,
    value=5,
    step=1,
)

number_of_people = int(number_of_people)

names = []
texts = []
for i in range(number_of_people):
    name = st.text_input(f"Name of person {i + 1}", key=f"name_{i}")
    text = st.text_input(f"Text of person {i + 1}", key=f"text_{i}")
    
    # Add the inputs to our lists
    names.append(name)
    texts.append(text)
# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.text_input("OpenAI API Key", type="password")

# If the user has provided their OpenAI API key, create an OpenAI instance.
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)


