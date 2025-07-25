import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="📊 Sentiment Dashboard", layout="wide")
st_autorefresh(interval=30 * 1000, key="datarefresh")

df = pd.read_csv("tweets.csv")
hashtag_df = pd.read_csv("hashtags_by_sentiment.csv")

# Split layout
col1, col2 = st.columns([1, 2])

# 👉 LEFT: About
with col1:
    st.markdown("## 🧠 About This Web App")
    st.write("""
    Welcome to the **Social Media Sentiment Analyzer**.

    - ⏳ Real-time update every 30 seconds
    - 💬 Tracks tweets and hashtags from X (Twitter)
    - 🟢🟡🔴 Performs sentiment analysis
    - ☁️ Generates word clouds and charts
    - 🛠️ Built with **Python + Streamlit**
    """)

    st.markdown("### 🔗 Powered By")
    st.markdown("""
    - TextBlob (Sentiment)
    - Matplotlib / WordCloud
    - Streamlit (Frontend)
    """)

# 👉 RIGHT: Snapshot (No filters)
with col2:
    st.markdown("## 🔍 Live Tweet Snapshot")

    latest = df.sort_values("Timestamp", ascending=False).head(5)
    latest_table = latest[["Timestamp", "Sentiment", "Clean_Text"]]

    st.markdown("""
    <style>
    .custom-table tbody tr:hover {background-color: #f6f6f6;}
    .custom-table td, .custom-table th {
        border: 1px solid #ddd !important;
        padding: 8px !important;
    }
    .custom-table thead {
        background-color: #dee2e6 !important;
        color: black !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.dataframe(
        latest_table.style
            .set_properties(**{
                'background-color': '#f0f2f6',
                'border-color': '#6c757d',
                'color': 'black',
                'border-radius': '10px',
            })
            .set_table_styles([
                {'selector': 'thead th', 'props': [('background-color', '#dee2e6')]},
                {'selector': 'tbody tr:nth-child(even)', 'props': [('background-color', '#e9ecef')]},
                {'selector': 'tbody tr:hover', 'props': [('background-color', '#ced4da')]},
            ])
    )

    st.markdown("### 🏷️ Trending Hashtags (Latest 5)")
    tags = hashtag_df.groupby("Hashtags").sum("Count").sort_values("Count", ascending=False).head(5)
    st.dataframe(
        tags.reset_index().style
        .set_properties(**{
            'background-color': '#f0f8ff',
            'border-color': '#343a40',
            'color': 'black'
        })
    )
