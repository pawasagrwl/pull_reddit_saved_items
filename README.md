# Reddit Saved Posts and Comments Fetcher

This Python script fetches your saved posts and comments from Reddit and saves them into a JSON file. It utilizes the PRAW (Python Reddit API Wrapper) library to access Reddit's API securely.

## Setup

### Prerequisites

- Python 3.6 or higher
- A Reddit account with API access

### Dependencies

Install the required Python packages using pip:

```bash
pip install praw python-dotenv
```

### Reddit API Credentials
    
1. Visit Reddit's App Preferences to create a new application.
2. Click on "Create App" or "Create Another App".
3. Fill out the form:
    - name: Your application's name
    - application type: Script
    - description: (Optional)
    - about url: (Optional)
    - permissions: (Optional)
    - redirect uri: http://localhost:8080 (or any valid URI)
4. Once created, you'll receive a client_id (below the application name) and a client_secret.

### Environment File

Create a .env file in the root directory of your script with the following content, replacing the placeholders with your actual Reddit API credentials and account details:

```js
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USERNAME=your_reddit_username
REDDIT_PASSWORD=your_reddit_password
```

## Usage

Run the script with Python:
```bash
python fetch_and_save_saved_posts_comments.py
```

This will fetch all your saved posts and comments from Reddit and save them into saved_items.json in the script's directory.

## JSON File Format

The JSON file contains a dictionary with two keys: last_pulled, indicating the last time the data was fetched, and content, containing the saved posts and comments. The content key is further divided into posts and comments, each a list of dictionaries containing the respective data.

### Posts

Each post is saved with the following information:

- title: The post title
- url: The full URL to the post on Reddit
- subreddit: The subreddit name
- body: The post's text content, if any
- media: The URL to the post's media, if any
- datetime: The post's creation date and time in UTC
- votes: The number of upvotes

### Comments

Each comment is saved with the following information:

- post_title: The title of the post the comment is on
- post_url: The full URL to the post
- post_media: The URL to the post's media, if any
- comment_url: The full URL to the comment on Reddit
- comment_text: The text of the comment
- datetime: The comment's creation date and time in UTC
- votes: The number of upvotes

## Note

Ensure you have the required permissions and adhere to Reddit's API usage rules and guidelines.