
# Reddit Saved Items Fetcher

This Python script fetches your saved posts and comments from Reddit, with an option to also fetch the top comments for each post on demand. It uses PRAW (Python Reddit API Wrapper) to securely access Reddit's API.

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

1. Visit [Reddit's App Preferences](https://www.reddit.com/prefs/apps) to create a new application.
2. Click on "Create App" or "Create Another App".
3. Fill out the form:
    - name: Your application's name
    - application type: Script
    - description: (Optional)
    - about url: (Optional)
    - permissions: (Optional)
    - redirect uri: http://localhost:8080 (or any valid URI)
4. Once created, note your `client_id` (below the application name) and `client_secret`.

### Environment File

Create a `.env` file in the root directory of your script with your Reddit API credentials and account details:

```js
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USERNAME=your_reddit_username
REDDIT_PASSWORD=your_reddit_password
```

## Usage

Run the script with Python:

```bash
python fetchItems.py
```

The script fetches all your saved posts and comments from Reddit. It will then prompt you about fetching comments for each post, warning about the time it may take based on the number of posts.


## JSON File Format

The JSON output (`saved_items.json`) has the following format

```json
{
  "last_pulled": "UTC timestamp of last fetch",
  "counts": {
    "subreddits": {
      "SubredditName": {
        "posts": 0,
        "comments": 0
      }
    },
    "votes": {
      "0-100": {
        "posts": 0,
        "comments": 0
      },
      "100-1000": {
        "posts": 0,
        "comments": 0
      },
      {"1000-10000": {
        "posts": 0,
        "comments": 0
      }},
      {"10000-100000": {
        "posts": 0,
        "comments": 0
      }},
      {"100000-1000000": {
        "posts": 0,
        "comments": 0
      }}

    },
    "dates": {
      "YYYY-MM": {
        "posts": 0,
        "comments": 0
      }
    }
  },
  "content": {
    "posts": [
      {
        "title": "Post Title",
        "url": "https://reddit.com/post_permalink",
        "subreddit": "SubredditName",
        "body": "Post Body",
        "media": "Post Media URL",
        "datetime": "Post Creation UTC",
        "votes": "Number of Upvotes",
        "top_comments": [
          {
            "comment_url": "https://reddit.com/comment_permalink",
            "comment_text": "Comment Body",
            "datetime": "Comment Creation UTC",
            "votes": "Number of Upvotes"
          }
        ]
      }
    ],
    "comments": [
      {
        "post_title": "Post Title",
        "post_subreddit": "SubredditName",
        "post_url": "https://reddit.com/post_permalink",
        "comment_url": "https://reddit.com/comment_permalink",
        "comment_text": "Comment Body",
        "datetime": "Comment Creation UTC",
        "votes": "Number of Upvotes"
      }
    ]
  }
}
```

## Developer Guide

To utilize this data in your code, load the JSON file with Python's `json` module. You can then iterate through `content["posts"]` and `content["comments"]` for posts and comments data, respectively. Use the `counts` and `last_pulled` information for analytics or display purposes.

```python
import json

with open('saved_items.json', 'r') as file:
    data = json.load(file)

# Example: Print titles of all saved posts
for post in data["content"]["posts"]:
    print(post["title"])
```

## Note

Ensure you have the required permissions and adhere to Reddit's API usage rules and guidelines.