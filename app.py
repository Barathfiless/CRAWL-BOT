import streamlit as st
import pandas as pd
from sentence_transformers import SentenceTransformer, util
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="Beast AI Search", page_icon="🔍", layout="wide")

# --- LOAD DATA & AI MODEL (CACHED) ---
@st.cache_resource
def load_resources():
    # Load the indexed data
    df = pd.read_pickle("processed_data.pkl")
    # Load AI Model
    model = SentenceTransformer('all-MiniLM-L6-v2')
    # Create Embeddings
    embeddings = model.encode(df['title'].tolist(), convert_to_tensor=True)
    return df, model, embeddings

try:
    df, model, embeddings = load_resources()
except Exception as e:
    st.error("Error: 'processed_data.pkl' file-ah kaanom! Modhalla Indexer-ah run pannunga.")
    st.stop()

# --- SIDEBAR ---
st.sidebar.title("⚙️ Search Settings")
top_n = st.sidebar.slider("Number of results", 5, 20, 10)
st.sidebar.info("This is an AI-powered Semantic Search Engine. It understands meaning, not just keywords.")

# --- MAIN UI ---
st.title("🕸️ Beast AI Search Engine")
st.markdown("Search across crawled pages using advanced **BERT Semantic Analysis**.")

# Search Bar
query = st.text_input("What are you looking for?", placeholder="e.g., How to learn Python")

if query:
    with st.spinner('AI is thinking...'):
        # 1. Semantic Search Logic
        query_embedding = model.encode(query, convert_to_tensor=True)
        hits = util.semantic_search(query_embedding, embeddings, top_k=top_n)
        
        # 2. Display Results
        st.subheader(f"Top {top_n} Semantic Results:")
        
        for hit in hits[0]:
            idx = hit['corpus_id']
            score = hit['score']
            title = df.iloc[idx]['title']
            url = df.iloc[idx]['url']
            
            # Result Card UI
            with st.container():
                st.markdown(f"### [{title}]({url})")
                st.caption(f"Confidence Score: {score:.4f} | Source: {url}")
                st.divider()
else:
    st.write("Enter a query to start searching.")

# --- FOOTER ---
st.markdown("---")
st.caption("Built with ❤️ using Python, Streamlit & BERT")
