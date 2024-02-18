from datetime import datetime
from dotenv import load_dotenv
import os
import praw
import json

# Load environment variables from .env file
load_dotenv()

def get_readable_datetime(utc_timestamp):
    """
    Convert a UTC timestamp to a human-readable datetime string.
    
    Parameters:
    - utc_timestamp: The UTC timestamp to convert.
    
    Returns:
    - A string representing the formatted datetime.
    """
    return datetime.utcfromtimestamp(utc_timestamp).strftime('%Y-%m-%d %H:%M:%S')

def fetch_saved_items():
    """
    Fetches saved posts and comments from a Reddit account and saves them to a JSON file.
    """
    # Initialize Reddit instance with credentials from environment variables
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        password=os.getenv("REDDIT_PASSWORD"),
        user_agent=f"Fetch Saved Posts and Comments by /u/{os.getenv('REDDIT_USERNAME')}",
        username=os.getenv("REDDIT_USERNAME"),
    )

    # Initialize structures to store fetched data
    saved_items = {"posts": [], "comments": []}
    subreddits = set()
    votes = []
    dates = []

    try:
        count = 0
        # Iterate through saved items in the Reddit account
        for item in reddit.user.me().saved(limit=None):
            count += 1
            print(f"{count} items processed", end='\r', flush=True)
            
            # Check if the item is a post or comment and process accordingly
            if hasattr(item, 'title'):  # Post
                post_data = {
                    "title": item.title,
                    "url": f"https://reddit.com{item.permalink}",
                    "subreddit": str(item.subreddit),
                    "body": item.selftext if item.selftext else "",
                    "media": item.url,
                    "datetime": get_readable_datetime(item.created_utc),
                    "votes": item.score
                }
                saved_items["posts"].append(post_data)
            else:  # Comment
                comment_data = {
                    "post_title": item.link_title,
                    "post_subreddit": str(item.subreddit),
                    "post_url": f"https://reddit.com{item.link_permalink}",
                    "comment_url": f"https://reddit.com{item.permalink}",
                    "comment_text": item.body,
                    "datetime": get_readable_datetime(item.created_utc),
                    "votes": item.score
                }
                saved_items["comments"].append(comment_data)

            # Collect subreddit names, votes, and dates for further analysis
            subreddits.add(str(item.subreddit if hasattr(item, 'subreddit') else item.submission.subreddit))
            votes.append(item.score)
            dates.append(item.created_utc)

        # Prepare the final output structure
        final_output = {
            "last_pulled": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            "content": {
                "subreddits": sorted(list(subreddits), key=str.lower),
                "least_votes": min(votes),
                "most_votes": max(votes),
                "earliest": get_readable_datetime(min(dates)),
                "latest": get_readable_datetime(max(dates)),
                "posts": saved_items["posts"],
                "comments": saved_items["comments"]
            }
        }

    except Exception as e:
        print(f"An error occurred: {e}")
        final_output = {}

    # Write the collected data to a JSON file
    with open("saved_items.json", "w") as outfile:
        json.dump(final_output, outfile, indent=4)
    print("\nFinished processing items.")

# Execute the main function to fetch and save Reddit saved items
if __name__ == "__main__":
    fetch_saved_items()
