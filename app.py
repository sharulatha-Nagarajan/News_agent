import streamlit as st
import os
from openai import OpenAI
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load the API key from the environment variable
API_KEY = os.getenv("XAI_API_KEY")

if not API_KEY:
    st.error("API key is missing! Please set the 'XAI_API_KEY' in the .env file.")
    st.stop()

# Initialize the OpenAI client
client = OpenAI(api_key=API_KEY, base_url="https://api.x.ai/v1")

# Streamlit app title
st.title("Top 5 News in Technology Categories")

# Dropdown options for categories
categories = [
    "Big Tech",
    "Global Tech",
    "SMB USA",
    "MSME India",
    "Startup India"
]

# User selects a category
selected_category = st.selectbox("Select a Category", categories)

# User selects a date
selected_date = st.date_input("Select a Date", datetime.today())

# Button to fetch news
if st.button("Get Latest News"):
    # Format the date to a readable format
    formatted_date = selected_date.strftime("%B %d, %Y")

    # Prompt based on selected category and date
    prompt_content = (
        f"Provide a list of the top 5 news items for {formatted_date}, strictly for today only (no older dates). "
        f"Categorize them under {selected_category}, including the event date for each item. "
        f"Ensure all news is fresh and relevant to the specified date."
    )

    try:
        # Request to the OpenAI API
        completion = client.chat.completions.create(
            model="grok-beta",
            messages=[
                {"role": "system", "content": "You are Grok, a chatbot to answer based on realtime data."},
                {"role": "user", "content": prompt_content},
            ],
        )

        # Extract the response content
        response_content = completion.choices[0].message.content

        # Display the output
        st.write("## Top 5 News in Technology and Trending Categories")
        st.write("=" * 60)

        # Try parsing the response as JSON
        try:
            news_data = json.loads(response_content)
            for category, articles in news_data.items():
                st.write(f"### Category: {category}")
                for i, article in enumerate(articles, 1):
                    st.write(f"**{i}. Title:** {article['title']}")
                    st.write(f"   **Date:** {article['date']}")
                    st.write(f"   **Description:** {article['description']}")
        except json.JSONDecodeError:
            # If the response is plain text, display it directly
            st.write(response_content)

    except Exception as e:
        st.error(f"Error fetching news: {e}")
