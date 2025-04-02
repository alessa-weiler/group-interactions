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

def simulate_conversation(person1_name, person1_text, person2_name, person2_text):
    """Simulate a conversation between two people using OpenAI API."""
    prompt = f"""
    Person 1 named {person1_name} has the following characteristics or background:
    {person1_text}
    
    Person 2 named {person2_name} has the following characteristics or background:
    {person2_text}
    
    Simulate a natural, brief conversation between these two people. 
    The conversation should reflect their characteristics.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "prompt": prompt}],
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error calling OpenAI API: {e}")
        return ""

def analyze_sentiment(conversation):
    """Analyze the sentiment of a conversation using OpenAI API."""
    prompt = f"""
    Analyze the sentiment of the following conversation on a scale from 0 to 100,
    where 0 is extremely negative and 100 is extremely positive.
    Return only the numeric score.
    
    Conversation:
    {conversation}
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "prompt": prompt}],
            max_tokens=10
        )
        sentiment_score = response.choices[0].message.content.strip()
        # Try to convert to float, default to 50 if it fails
        try:
            return float(sentiment_score)
        except ValueError:
            return 50.0
    except Exception as e:
        st.error(f"Error analyzing sentiment: {e}")
        return 50.0

def summarize_conversation(conversation):
    """Generate a brief summary of the conversation using OpenAI API."""
    prompt = f"""
    Provide a brief one-sentence summary of the following conversation:
    
    {conversation}
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "prompt": prompt}],
            max_tokens=100
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Error summarizing conversation: {e}")
        return "Summary not available."

# If the user has provided their OpenAI API key, create an OpenAI instance.
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)
    # Create a progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Create lists to store results
    person1_list = []
    person2_list = []
    sentiment_scores = []
    summaries = []
    
    # Calculate total number of conversation pairs
    total_pairs = (number_of_people * (number_of_people - 1)) // 2
    current_pair = 0
    
    # Simulate conversations for all unique pairs
    for i in range(number_of_people):
        for j in range(i+1, number_of_people):
            current_pair += 1
            
            status_text.text(f"Simulating conversation between {names[i]} and {names[j]} ({current_pair}/{total_pairs})")
            progress_bar.progress(current_pair / total_pairs)
            
            # Simulate the conversation
            conversation = simulate_conversation(names[i], texts[i], names[j], texts[j])
            
            # Analyze sentiment
            sentiment = analyze_sentiment(conversation)
            
            # Summarize conversation
            summary = summarize_conversation(conversation)
            
            # Store results
            person1_list.append(names[i])
            person2_list.append(names[j])
            sentiment_scores.append(sentiment)
            summaries.append(summary)
            
            # Add a small delay to avoid hitting API rate limits
            time.sleep(1)
    
    # Create the dataframe
    conversations_df = pd.DataFrame({
        'Person1': person1_list,
        'Person2': person2_list,
        'Sentiment': sentiment_scores,
        'Summary': summaries
    })
    
    # Display the dataframe
    st.subheader("Conversation Results")
    st.dataframe(conversations_df)

