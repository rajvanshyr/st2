import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
import streamlit.components.v1 as components
import anthropic

# Page title
client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key="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",
)

st.set_page_config(page_title='Interactive Data Explorer', page_icon='📊')
st.title('📊 Interactive Data Explorer ayyy2')

with st.sidebar:
    anthropic_api_key = st.text_input("Openai API Key", key="file_qa_api_key", type="password")

with st.expander('About this app'):
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
niche_list=['Real Estate','Growth', 'Crypto', 'Finance', 'Artfifical Intellgence', 'Self-Improvement']
genres_selection = st.multiselect('Select genres', niche_list, ['Growth', 'Crypto' ])

## Year selection
year_list = df.year.unique()
txt1 = st.text_area(
    "Original tweet",
    "Write What you want up here",)

txt2 = st.text_area(
    "What are you looking to improve?",
    "Write What you want up here",)

year_selection = st.slider('Select year temp', 0.0, 1.0,.5)
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

year_selection_list = list(np.arange(year_selection[0], year_selection[1]+1))

df_selection = df[df.genre.isin(genres_selection) & df['year'].isin(year_selection_list)]
reshaped_df = df_selection.pivot_table(index='year', columns='genre', values='gross', aggfunc='sum', fill_value=0)
reshaped_df = reshaped_df.sort_values(by='year', ascending=False)

title = st.text_input('Movie title', 'Life of Brian')
st.write('The current movie title is', title)
# Display DataFrame

df_editor = st.data_editor(reshaped_df, height=212, use_container_width=True,
                            column_config={"year": st.column_config.TextColumn("Year")},
                            num_rows="dynamic")
df_chart = pd.melt(df_editor.reset_index(), id_vars='year', var_name='genre', value_name='gross')

# Display chart
chart = alt.Chart(df_chart).mark_line().encode(
            x=alt.X('year:N', title='Year'),
            y=alt.Y('gross:Q', title='Gross earnings ($)'),
            color='genre:N'
            ).properties(height=320)
st.altair_chart(chart, use_container_width=True)
