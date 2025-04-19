# News Watchlist App

A Streamlit application that allows users to manage a watchlist of keywords and fetch relevant news articles using the News API.

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the root directory and add your News API key:
```
NEWS_API_KEY=your_api_key_here
```

You can get a free API key from [News API](https://newsapi.org/).

## Running the App

To run the app, execute:
```bash
streamlit run app.py
```

## Features

- Add and remove keywords from your watchlist
- Select multiple keywords to search for news
- View news articles from the past 2 days
- Each article displays:
  - Title
  - Source
  - Publication date
  - Description
  - Link to full article
  - Image (if available)
