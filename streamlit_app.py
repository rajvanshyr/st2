import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
import streamlit.components.v1 as components
import anthropic

# Page title


st.set_page_config(page_title='Interactive Data Explorer', page_icon='📊')
st.title('📊 Interactive Data Explorer ayyy2')

with st.sidebar:
		anthropic_api_key = st.text_input("Anthropic API Key", key="file_qa_api_key", type="password")


client = anthropic.Anthropic(
		# defaults to os.environ.get("ANTHROPIC_API_KEY")
		api_key=anthropic_api_key,
)
r="dd"

	#r=message.content
with st.expander('About this app'+str(r)):
	st.markdown('**What can this app do?**')
	st.info('This app shows the use of Pandas for data wrangling, Altair for chart creation and editable dataframe for data interaction.')
	st.markdown('**How to use the app?**')
	st.warning('To engage with the app, 1. Select genres of your interest in the drop-down selection box and then 2. Select the year duration from the slider widget. As a result, this should generate an updated editable DataFrame and line plot.')
	
st.subheader('Which Movie Genre performs ($) best at the box office?')

# Load data
df = pd.read_csv('data/movies_genres_summary.csv')
df.year = df.year.astype('int')

# Input widgets
## Genres selection
#genres_list = df.genre.unique()
niche_list=['Real Estate','Growth', 'Crypto', 'Finance', 'Artfifical Intellgence', 'Self-Improvement', 'Social Justice']
genres_selection = st.multiselect('Select genres', niche_list, ['Growth', 'Crypto' ])

## Year selection
year_list = df.year.unique()
txt1 = st.text_area(
		"Original tweet",
		"Write What you want up here",)

txt2 = st.text_area(
		"What are you looking to improve?",
		"Write What you want up here",)

temp_selection = st.slider('Select year temp', 0.0, 1.0,.5)
if st.button('Generate') and anthropic_api_key:
	u_prompt = f"Generate a clever tweet appealing to the following Niche: {genres_selection}"
	if txt1:
		u_prompt=u_prompt+" This is the current tweet: "+txt1
		if txt2:
			u_prompt=u_prompt=u_prompt+" This is what the user wants to improve: "+txt2
	st.markdown('Prompt: '+ u_prompt)
	message = client.messages.create(
		model="claude-3-sonnet-20240229",
		max_tokens=499,
		temperature=0,
		system="You are a highly skilled marketing expert specializing in crafting engaging and effective Twitter posts to help users build a strong personal brand on the platform.\"\n\"Follow these guidelines when generating posts:\"\n\"1. Always start with a compelling hook on the first line to capture the reader's attention.\"\n\"2. Limit posts to 280 characters or less to adhere to Twitter's character limit.\"\n\"3. Use up to 3 relevant emojis per post to add visual appeal and convey emotion, but avoid overusing them.\"\n\"4. Incorporate the topics and extra details provided in the user prompt to ensure the post is tailored to their specific needs.\"\n“5. Maintain a consistent brand voice and tone that aligns with the user's personal brand.\"\n“6. Provide valuable insights, tips, or entertaining content that resonates with the target audience.\"\n\"Output the generated post in JSON format with the following keys:\"\n\"content: The full Twitter post, with the content properly escaped and formatted. Replace newline characters with spaces.\"\n\"keywords: A list of 5-7 relevant keywords for the post to optimize for search and discoverability.\"\n\"title: A concise and descriptive title for the post, up to 60 characters, for internal reference in the CMS.\"\n“areasOfImprovment:The top way the post can be further improved”",
		messages=[
				{
						"role": "user",
						"content": [
								{
										"type": "text",
										"text": u_prompt
								},                 # Prefill Claude's response to force JSON output
						]
				},                
				{
										"role": "assistant",
										"content": "{",
								}, 
		],
		)

st.markdown("reponse:" + message.content)
components.html(
		"""

<title>Twitter Post</title>
</head>
<body>

<!-- Button to post to Twitter -->
<button id="twitterPostBtn">Post to Twitter</button>

<!-- Script to handle the button click and redirect to Twitter -->
<script>
		document.getElementById('twitterPostBtn').addEventListener('click', function() {
				var tweetContent = "{{ tweet_content }}"; // Content generated in the Flask app
				var twitterUrl = "https://twitter.com/intent/tweet?text=" + encodeURIComponent(tweetContent);
				window.open(twitterUrl, '_blank');
		});
</script>
		""", height=600,
		)
