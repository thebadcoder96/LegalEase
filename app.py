import asyncio
import streamlit as st

from src.scrape import scrape
from src.analyze import analyze_document


st.title("LegalEase")

st.write("Enter a URL containing legal text:")
url = st.text_input("URL", key="url", placeholder="https://policies.google.com/privacy")

if url:
    with st.spinner("Scraping..."):
        doc = asyncio.run(scrape(url))
        st.success(f"Scraped {doc['source']}")
    with st.spinner("Analyzing..."):
        analysis = analyze_document(doc['content'])
        st.success(f"Analyzed {doc['source']}")
        st.subheader("Analysis:")
        st.write(analysis)

