import asyncio
import streamlit as st

from src.scrape import scrape
from src.analyze import analyze_document

def render_dict(data, level=0):
    for key, value in data.items():
        if isinstance(value, dict):
            st.subheader("  " * level + key)
            render_dict(value, level + 1)
        elif isinstance(value, list):
            st.subheader("  " * level + key)
            for item in value:
                if isinstance(item, dict):
                    with st.expander(f"{item.get('category', '')} {item.get('point', '')}".strip()):
                        render_dict(item, level + 1)
                else:
                    st.write("  " * (level + 1) + str(item))
        else:
            st.write("  " * level + f"**{key}:** {value}")

st.title("LegalEase")

st.write("Enter a URL containing legal text:")
url = st.text_input("URL", key="url", placeholder="https://policies.google.com/privacy")

if url:
    with st.spinner("Scraping..."):
        doc = asyncio.run(scrape(url))
        st.success(f"Scraped {doc['source']}")
    with st.spinner("Analyzing..."):
        analysis = analyze_document(doc['content'])
        st.success(f"Analyzed {doc['title']}")
        st.subheader("Analysis:")
        render_dict(analysis)
        with st.expander("JSON output:"):
            st.write(analysis)

