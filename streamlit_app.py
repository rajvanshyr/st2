import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
import streamlit.components.v1 as components
import anthropic
import webbrowser
import urllib.parse
import json

# Page title
st.set_page_config(page_title='Generate a Viral tweet', page_icon='📊')
st.title('Generate a Viral tweet')

with st.sidebar:
    anthropic_api_key = st.text_input("Anthropic API Key", key="file_qa_api_key", type="password")

client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key=anthropic_api_key,
)

with st.expander('About this app'):
    st.markdown('**What can this app do?**')
    st.info('This app shows the use of Prompting and Human augmented generation to generate tweets')
    st.markdown('**How to use the app?**')
    st.warning('To engage with the app, 1. Select niche of your interest in the drop-down selection box and then 2. Put in your initial tweet and any areas you want to improve')

st.subheader('Which Niche do you want to appeal to?')

# Load data
df = pd.read_csv('data/movies_genres_summary.csv')
df.year = df.year.astype('int')

# Input widgets
## Genres selection
niche_list = ['Real Estate', 'Growth', 'Crypto', 'Finance', 'Artificial Intelligence', 'Self-Improvement', 'Social Justice']
genres_selection = st.multiselect('Select genres', niche_list, ['Growth', 'Crypto'])

## Year selection
year_list = df.year.unique()
txt1 = st.text_area("Original tweet", "Write What you want up here")
txt2 = st.text_area("What are you looking to improve?", "Write What you want up here")

temp_selection = st.slider('Select year temp(how crazy the model can be)', 0.0, 1.0, 0.5)

if 'generate_clicked' not in st.session_state:
    st.session_state.generate_clicked = False

if 'post_clicked' not in st.session_state:
    st.session_state.post_clicked = False

if st.button('Generate') and anthropic_api_key:
    st.session_state.generate_clicked = True
    u_prompt = f"Generate a clever tweet appealing to the following Niche: {genres_selection}"
    if txt1:
        u_prompt = u_prompt + " This is the current tweet: " + txt1
        if txt2:
            u_prompt = u_prompt + " This is what the user wants to improve: " + txt2
    st.markdown('Prompt: ' + u_prompt)
    message = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=499,
        temperature=0,
        system="You are a highly skilled marketing expert specializing in crafting engaging and effective Twitter posts\
         to help users build a strong personal brand on the platform.Follow these guidelines when generating\
            posts:1. Always start with a compelling hook on the first line to capture the reader's attention.2. \
            Limit posts to 280 characters or less to adhere to Twitter's character limit.\
            3. Use up to 3 relevant emojis per post to add visual appeal and convey emotion, \
            but avoid overusing them.4. Incorporate the topics and extra details provided in the user prompt to ensure the post is tailored to their specific \
            needs. 5. Maintain a consistent brand voice and tone that aligns with the user's personal brand.6. Provide valuable insights, \
            tips, or entertaining content that resonates with the target audience.Output the generated post in JSON format with the following \
            keys:content: The full Twitter post, with the content properly escaped and formatted. \
            Replace newline characters with spaces.keywords: A list of 5-7 relevant keywords for the post to optimize for search and \
            discoverability.title: A concise and descriptive title for the post, up to 60 characters, for internal reference in the \
            CMS.areasOfImprovment:The top way the post can be further improved",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": u_prompt
                    },
                ]
            },
            {
                "role": "assistant",
                "content": "{",
            },
        ],
    )
    ux = str(message.content)
    st.markdown("Response:" + str(ux))
    # Parse the JSON response
    try:
        tweet_content = ux
        st.markdown("Generated Tweet:")
        st.info(tweet_content)
        
        # URL-encode the tweet content
        encoded_tweet = urllib.parse.quote(tweet_content)
        
        # Create the Twitter URL with the tweet content
        twitter_url = f"https://twitter.com/intent/tweet?text={encoded_tweet}"
        
        # Display a button to post the tweet
        if st.button('Post to Twitter'):
            st.session_state.post_clicked = True
            webbrowser.open(twitter_url)
    except json.JSONDecodeError:
        st.error("Invalid JSON response from the API.")

else:
    if not anthropic_api_key:
        st.warning('Please add your Anthropic API key to continue.')