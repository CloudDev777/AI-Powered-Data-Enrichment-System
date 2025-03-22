# modules/search_engine.py
import os
from dotenv import load_dotenv

# Fix the import issue with SerpAPI
try:
    from serpapi import GoogleSearch
except ImportError:
    try:
        # Alternative import path
        from serpapi.google_search import GoogleSearch
    except ImportError:
        # If that fails too, try the google-search-results package
        from google_search_results import GoogleSearch

load_dotenv()

class SearchEngine:
    def __init__(self):
        self.api_key = os.getenv("SERPAPI_API_KEY")
        
    def search(self, query, num_results=5):
        """Perform web search using SerpAPI"""
        if not self.api_key:
            raise ValueError("SERPAPI_API_KEY not found in environment variables")
        
        try:
            search_params = {
                "q": query,
                "num": num_results,
                "api_key": self.api_key
            }
            
            search = GoogleSearch(search_params)
            results = search.get_dict()
            
            # Extract organic results
            organic_results = results.get("organic_results", [])
            
            # Format results for LLM processing
            formatted_results = []
            for result in organic_results:
                formatted_results.append({
                    "title": result.get("title", ""),
                    "link": result.get("link", ""),
                    "snippet": result.get("snippet", "")
                })
            
            return formatted_results
        except Exception as e:
            print(f"Error performing search: {e}")
            return []
