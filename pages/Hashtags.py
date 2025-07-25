import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="🏷️ Hashtag Explorer", layout="wide")
st.title("🏷️ Hashtag Analysis")

# Load data
hashtags_df = pd.read_csv("hashtags_by_sentiment.csv")

# Filter
sentiments = st.multiselect("🧠 Select Sentiment", ["Positive", "Neutral", "Negative"], default=[])
if not sentiments:
    st.warning("⚠️ Please select at least one sentiment.")
    st.stop()

filtered = hashtags_df[hashtags_df["Sentiment"].isin(sentiments)]

# Chart Section
st.subheader("📊 Top Hashtags by Sentiment")

for sentiment in sentiments:
    top_tags = (
        filtered[filtered["Sentiment"] == sentiment]
        .sort_values("Count", ascending=False)
        .head(10)
    )

    if not top_tags.empty:
        st.markdown(f"#### 🔹 {sentiment} Hashtags")
        fig, ax = plt.subplots()
        ax.barh(top_tags["Hashtags"], top_tags["Count"], color="#5f9ea0")
        ax.set_xlabel("Count")
        ax.set_ylabel("Hashtag")
        ax.invert_yaxis()
        st.pyplot(fig)
    else:
        st.info(f"ℹ️ No hashtags found for {sentiment}.")

# 💡 Styled Table Function
def styled_table(df):
    return st.dataframe(
        df.style
        .set_properties(**{
            'background-color': '#f7f9fb',
            'color': '#212529',
            'border-color': '#adb5bd',
            'border-radius': '10px',
        })
        .set_table_styles([
            {'selector': 'thead th', 'props': [('background-color', '#cfe2ff')]},
            {'selector': 'tbody tr:nth-child(even)', 'props': [('background-color', '#e2eafc')]},
            {'selector': 'tbody tr:hover', 'props': [('background-color', '#dbe7f5')]},
        ])
    )

# Full Table
st.subheader("📄 Hashtag Table View")
styled_table(filtered)
