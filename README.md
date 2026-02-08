# Beast Search: High-Speed Keyword Search Engine

A professional, modular search engine pipeline that performs web crawling, data indexing, and keyword-based ranking. This version is optimized for speed and uses traditional TF-IDF (Term Frequency-Inverse Document Frequency) for ranking results.

---

## Project Structure

The project consists of 4 specialized Python modules:

1.  **`crawler.py`**: The Data Gatherer. Uses asynchronous requests to scrape titles, URLs, and download images.
2.  **`indexer.py`**: The Data Processor. Cleans raw HTML text, removes stopwords, and prepares an optimized index.
3.  **`search_engine.py`**: The Brain. Implements the **TF-IDF Ranking Algorithm** to match queries with the most relevant pages.
4.  **`app.py`**: The Interface. A clean and responsive Web UI built with **Streamlit**.

---

## Features

* **Asynchronous Crawling:** High-speed data gathering using `aiohttp`.
* **Keyword Ranking:** Uses Mathematical Similarity (Cosine Similarity) to find the best matches.
* **Lightweight:** No heavy AI models; runs fast on any computer with minimal RAM.
* **Media Support:** Automatically harvests images from crawled pages into a dedicated folder.



---

## Installation & Setup

### 1. Requirements
Install the necessary Python libraries:
```
pip install asyncio aiohttp beautifulsoup4 lxml pandas nltk scikit-learn streamlit
```

2. NLP Setup
The indexer needs the NLTK dataset to filter out common words (the, is, at, etc.):
```
Python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

How to Run
Follow these steps in order:

Step 1: Gather Data
Run the crawler to visit websites and save the data to a CSV file.

```
python crawler.py
```

Step 2: Index the Data
Clean the raw data and prepare it for fast searching.

```
python indexer.py
```

Step 3: Launch the Search App
Start the web interface to browse your results.

```
streamlit run app.py
```
