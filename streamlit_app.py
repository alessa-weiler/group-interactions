import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("Group Interactions")
st.write(
    "This is a simple app that uses OpenAI's GPT-3.5 model to simulate group dynamics. "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
    "You can also learn how to build this app step by step by [following our tutorial](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)."
)
number_of_people = st.number_input(
    "Number of people in the group",
    min_value=1,
    max_value=10,
    value=5,
    step=1,
)
# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.text_input("OpenAI API Key", type="password")


