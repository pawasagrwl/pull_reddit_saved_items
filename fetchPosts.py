from datetime import datetime
from dotenv import load_dotenv
import os
import praw
import json

load_dotenv()  # Load environment variables from .env file

def get_readable_datetime(utc_timestamp):
    """Convert UTC timestamp to a readable datetime string."""
    return datetime.utcfromtimestamp(utc_timestamp).strftime('%Y-%m-%d %H:%M:%S')

def fetch_and_save_saved_posts_comments_fast():
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        password=os.getenv("REDDIT_PASSWORD"),
        user_agent=f"Fetch Saved Posts and Comments by /u/{os.getenv('REDDIT_USERNAME')}",
        username=os.getenv("REDDIT_USERNAME"),
    )

    saved_items = {"posts": [], "comments": []}
    subreddits = set()
    votes = []
    dates = []

    try:
        count = 0
        for item in reddit.user.me().saved(limit=None):
            count += 1
            print(f"{count} items processed", end='\r', flush=True)
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

            subreddits.add(str(item.subreddit if hasattr(item, 'subreddit') else item.submission.subreddit))
            votes.append(item.score)
            dates.append(item.created_utc)

        # Prepare final structure after collecting all data
        final_output = {
            "last_pulled": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            "content": {
                "subreddits": list(subreddits),
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

    # Writing to file once at the end
    with open("../public/saved_items.json", "w") as outfile:
        json.dump(final_output, outfile, indent=4)

    print("\nFinished processing items.")

fetch_and_save_saved_posts_comments_fast()
