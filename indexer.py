import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pickle
import os

# NLTK requirements
nltk.download('punkt')
nltk.download('stopwords')

class SearchIndexer:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.stop_words = set(stopwords.words('english'))

    def clean_text(self, text):
        if not isinstance(text, str): return ""
        tokens = word_tokenize(text.lower())
        # Clean symbols and stopwords
        cleaned = [w for w in tokens if w.isalnum() and w not in self.stop_words]
        return " ".join(cleaned)

    def process_and_save(self):
        print(f"Loading {self.csv_file}...")
        df = pd.read_csv(self.csv_file)
        
        print("Cleaning titles for indexing...")
        df['clean_title'] = df['title'].apply(self.clean_text)
        
        # Intha cleaned data-va oru special format-la save panrom
        df.to_pickle("processed_data.pkl")
        print("Indexing Complete! Processed data saved as 'processed_data.pkl'")

if __name__ == "__main__":
    # Unga Crawler kudutha CSV file name inga irukanum
    indexer = SearchIndexer('beast_media_final_results.csv')
    indexer.process_and_save()
