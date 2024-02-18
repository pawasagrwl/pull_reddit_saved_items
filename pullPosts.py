from datetime import datetime
from dotenv import load_dotenv
import os
import praw
import json

load_dotenv()  # Load environment variables from .env file

def get_readable_datetime(utc_timestamp):
    """Convert UTC timestamp to a readable datetime string."""
    return datetime.utcfromtimestamp(utc_timestamp).strftime('%Y-%m-%d %H:%M:%S')

def fetch_and_save_saved_posts_comments():
    try:
        reddit = praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            password=os.getenv("REDDIT_PASSWORD"),
            user_agent=f"Fetch Saved Posts and Comments by /u/{os.getenv('REDDIT_USERNAME')}",
            username=os.getenv("REDDIT_USERNAME"),
        )

        saved_items = {"posts": [], "comments": []}
        count = 0
        for item in reddit.user.me().saved(limit=None):
            count += 1
            print(f"{count} items processed", end='\r', flush=True)
            
            if hasattr(item, 'title'):  # This is a post
                post_data = {
                    "title": item.title,
                    "url": f"https://reddit.com{item.permalink}",  # Ensures post URL is the Reddit link
                    "subreddit": str(item.subreddit),
                    "body": item.selftext if item.selftext else "no body content",
                    "media": item.url,  # Directly use item.url for media
                    "datetime": get_readable_datetime(item.created_utc),  # Convert UTC timestamp to readable datetime
                    "votes": item.score  # Number of votes
                }
                saved_items["posts"].append(post_data)
            else:  # This is a comment
                comment_data = {
                    "post_title": item.submission.title,
                    "post_url": f"https://reddit.com{item.submission.permalink}",  # Use permalink for consistency
                    "post_media": item.submission.url,
                    "comment_url": f"https://reddit.com{item.permalink}",
                    "comment_text": item.body,
                    "datetime": get_readable_datetime(item.created_utc),  # Convert UTC timestamp to readable datetime
                    "votes": item.score  # Number of votes
                }
                saved_items["comments"].append(comment_data)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print(f"\nProcessed {count} items in total.")
        final_output = {
            "last_pulled": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            "content": saved_items
        }
        try:
            with open("saved_items.json", "w") as outfile:
                json.dump(final_output, outfile, indent=4)
        except Exception as e:
            print(f"Failed to save data to file: {e}")

fetch_and_save_saved_posts_comments()
