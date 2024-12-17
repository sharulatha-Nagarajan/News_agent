import streamlit as st
import os
from openai import OpenAI
import json
from datetime import datetime

# Streamlit app title
st.title("Top 5 News in Technology Categories")

# Input for API Key
XAI_API_KEY = st.text_input("Enter Your API Key", type="password")  # Use 'password' type to mask the input

# If the API key is provided, show a confirmation message
if XAI_API_KEY:
    st.success("API Key provided! You can now select the category and date to fetch news.")
else:
    st.warning("Please enter your OpenAI API key to proceed.")

# Ensure the API key is provided before proceeding
if XAI_API_KEY:
    # Initialize the OpenAI client
    client = OpenAI(api_key=XAI_API_KEY, base_url="https://api.x.ai/v1")

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

