import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pickle

class RankerEngine:
    def __init__(self, pkl_file):
        # 1. Load the indexed data
        self.df = pd.read_pickle(pkl_file)
        self.vectorizer = TfidfVectorizer()
        
        # 2. Build the Ranking Matrix (The Brain)
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df['clean_title'])
        self.stop_words = set(stopwords.words('english'))

    def clean_query(self, query):
        tokens = word_tokenize(query.lower())
        cleaned = [w for w in tokens if w.isalnum() and w not in self.stop_words]
        return " ".join(cleaned)

    def search(self, query, top_n=5):
        cleaned_query = self.clean_query(query)
        query_vec = self.vectorizer.transform([cleaned_query])
        
        # Ranking Logic: Cosine Similarity
        scores = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
        
        self.df['score'] = scores
        # Rank by highest score
        results = self.df[self.df['score'] > 0].sort_values(by='score', ascending=False)
        return results[['title', 'url', 'score']].head(top_n)

if __name__ == "__main__":
    engine = RankerEngine("processed_data.pkl")
    
    while True:
        q = input("\nEnter Search Query (exit to stop): ")
        if q.lower() == 'exit': break
        
        res = engine.search(q)
        if not res.empty:
            print(f"\nFound {len(res)} relevant results:")
            for i, row in res.iterrows():
                print(f"[{i}] {row['title']} \n    URL: {row['url']} \n    Rank Score: {row['score']:.4f}\n")
        else:
            print("No matching results found.")
