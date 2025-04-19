import streamlit as st
from serpapi import GoogleSearch
from datetime import datetime, timedelta
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants
SERP_API_KEY = os.getenv('SERP_API_KEY')
WATCHLIST_FILE = 'watchlist.json'

# Initialize watchlist from file if it exists
def load_watchlist():
    if os.path.exists(WATCHLIST_FILE):
        with open(WATCHLIST_FILE, 'r') as f:
            return json.load(f)
    return []

def save_watchlist(watchlist):
    with open(WATCHLIST_FILE, 'w') as f:
        json.dump(watchlist, f)


# Initialize session state for watchlist
if 'watchlist' not in st.session_state:
    st.session_state.watchlist = load_watchlist()

def fetch_news(keywords):
    # Calculate date range (last 2 days)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=2)
    
    # Format dates for API
    from_date = start_date.strftime('%Y-%m-%d')
    to_date = end_date.strftime('%Y-%m-%d')
    
    # Create query string
    query = ' OR '.join(keywords)
    
    
    # Fetch news using SerpAPI
    try:
        # params = {
        #     "engine": "google",
        #     "q": query,
        #     "tbm": "nws",  # news search
        #     "api_key": SERP_API_KEY,
        #     "tbs": f"cdr:1,cd_min:{from_date},cd_max:{to_date}",
        #     "num": 20  # number of results
        # }
        params = {
                "engine": "google_news",
                "q": query,
                "api_key": SERP_API_KEY,
                }
        
        search = GoogleSearch(params)
        results = search.get_dict()
        print('results keys: ', results.keys())
        
        if "news_results" not in results:
            return []
            
        articles = []
        for result in results["news_results"]:
            # print('result keys: ', result)
            for k, v in result.items():
                print(f'{k} -> {v}' )
            article = {
                "title": result.get("title", ""),
                "source": {"name": result["source"]['name']},
                "publishedAt": result.get("date", ""),
                "description": result.get("snippet", ""),
                "url": result.get("link", ""),
                "urlToImage": result.get("thumbnail", "")
            }
            articles.append(article)
        
        
        return articles
    except Exception as e:
        st.error(f"Error fetching news: {str(e)}")
        return []

def main():
    st.title("News Watchlist App")
    
    # Sidebar for watchlist management
    with st.sidebar:
        st.header("Manage Watchlist")
        
        # Add keyword
        new_keyword = st.text_input("Add a new keyword")
        if st.button("Add"):
            if new_keyword and new_keyword not in st.session_state.watchlist:
                st.session_state.watchlist.append(new_keyword)
                save_watchlist(st.session_state.watchlist)
                st.success(f"Added '{new_keyword}' to watchlist")
        
        # Display and manage existing keywords
        st.subheader("Your Watchlist")
        for keyword in st.session_state.watchlist:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(keyword)
            with col2:
                if st.button("Delete", key=f"del_{keyword}"):
                    st.session_state.watchlist.remove(keyword)
                    save_watchlist(st.session_state.watchlist)
                    st.rerun()
    
    # Main content area
    st.header("News Articles")
    
    if not st.session_state.watchlist:
        st.info("Add some keywords to your watchlist to see news articles.")
    else:
        # Multiselect for choosing keywords to search
        selected_keywords = st.multiselect(
            "Select keywords to search",
            st.session_state.watchlist,
            default=st.session_state.watchlist
        )
        
        if selected_keywords:
            if st.button("Search News"):
                with st.spinner("Fetching news articles..."):
                    articles = fetch_news(selected_keywords)
                    
                    if not articles:
                        st.warning("No articles found for the selected keywords.")
                    else:
                        for article in articles:
                            st.markdown("---")
                            st.subheader(article['title'])
                            st.write(f"**Source:** {article['source']['name']}")
                            st.write(f"**Published:** {article['publishedAt']}")
                            st.write(article['description'])
                            if article['url']:
                                st.markdown(f"[Read more]({article['url']})")

if __name__ == "__main__":
    main() 