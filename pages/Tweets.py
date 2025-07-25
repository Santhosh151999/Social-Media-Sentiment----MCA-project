import streamlit as st
import pandas as pd

st.set_page_config(page_title="📝 Tweet Explorer", layout="wide")
st.title("📝 Tweets Viewer & Export")

# Load data
df = pd.read_csv("tweets.csv")

# Sidebar Filters
st.sidebar.header("🔍 Filters")
sentiments = st.sidebar.multiselect("🧠 Sentiment", ["Positive", "Neutral", "Negative"], default=[])
keyword = st.sidebar.text_input("🔎 Search keyword or hashtag")

# Filter logic
filtered_df = df[df["Sentiment"].isin(sentiments)]
if keyword:
    keyword_lower = keyword.lower()
    filtered_df = filtered_df[
        filtered_df["Clean_Text"].str.lower().str.contains(keyword_lower) |
        filtered_df["Text"].str.lower().str.contains(keyword_lower)
    ]

# Guard clause
if not sentiments:
    st.warning("⚠️ Please select at least one sentiment.")
    st.stop()

# 💡 Styled Table Function
def styled_table(df):
    return st.dataframe(
        df.style
        .set_properties(**{
            'background-color': '#f6fbf9',
            'color': '#1c1c1c',
            'border-color': '#a0a0a0',
        })
        .set_table_styles([
            {'selector': 'thead th', 'props': [('background-color', '#d1e7dd')]},
            {'selector': 'tbody tr:nth-child(even)', 'props': [('background-color', '#e9f7ef')]},
            {'selector': 'tbody tr:hover', 'props': [('background-color', '#cfe3d6')]},
        ])
    )

# Table
st.subheader("📄 Filtered Tweets Table")
styled_table(filtered_df[["Timestamp", "Sentiment", "Clean_Text"]])

# Export
st.download_button(
    label="📥 Download Filtered Tweets as CSV",
    data=filtered_df.to_csv(index=False).encode("utf-8"),
    file_name="filtered_tweets.csv",
    mime="text/csv"
)
