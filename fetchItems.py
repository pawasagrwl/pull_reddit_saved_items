from datetime import datetime
from dotenv import load_dotenv
import os, praw, json, time

# Load environment variables from .env file
load_dotenv()

BOLD = '\033[1m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def get_readable_datetime(utc_timestamp):
    return datetime.utcfromtimestamp(utc_timestamp).strftime('%Y-%m-%d %H:%M:%S')

def initialize_counts(vote_ranges):
    """Initialize the structure for counting posts and comments separately."""
    
    counts = {
        "subreddits": {},
        "votes": {f"{range_[0]}-{range_[1]}": {"posts": 0, "comments": 0} for range_ in vote_ranges},
        "dates": {}
    }
    return counts

def update_counts(counts, item, is_post, vote_ranges):
    """Update counts for subreddits, votes, and dates based on the item."""
    
    type_ = "posts" if is_post else "comments"
    subreddit_name = str(item.subreddit if hasattr(item, 'subreddit') else item.submission.subreddit)
    subreddit_counts = counts["subreddits"].setdefault(subreddit_name, {"posts": 0, "comments": 0})
    subreddit_counts[type_] += 1

    for range_ in vote_ranges:
        range_key = f"{range_[0]}-{range_[1]}"
        if range_[0] <= item.score < range_[1]:
            counts["votes"][range_key][type_] += 1
            break

    year_month = datetime.utcfromtimestamp(item.created_utc).strftime('%Y-%m')
    date_counts = counts["dates"].setdefault(year_month, {"posts": 0, "comments": 0})
    date_counts[type_] += 1

def fetch_saved_items():
    
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        password=os.getenv("REDDIT_PASSWORD"),
        user_agent=f"Fetch Saved Posts and Comments by /u/{os.getenv('REDDIT_USERNAME')}",
        username=os.getenv("REDDIT_USERNAME"),
    )

    saved_items = {"posts": [], "comments": []}
    vote_ranges = [(0, 100), (100, 1000), (1000, 10000), (10000, 100000), (100000, 1000000)]
    counts = initialize_counts(vote_ranges)

    try:
        count = 0
        start_time = time.time()  # Capture start time
        for item in reddit.user.me().saved(limit=None):
            count += 1
            print(f"{count} items processed", end='\r', flush=True)

            is_post = hasattr(item, 'title')
            update_counts(counts, item, is_post, vote_ranges)
            
            if is_post:  # Post
                post_data = {
                    "title": item.title,
                    "url": f"https://reddit.com{item.permalink}",
                    "subreddit": str(item.subreddit),
                    "body": item.selftext if item.selftext else "",
                    "media": item.url,
                    "datetime": get_readable_datetime(item.created_utc),
                    "votes": item.score,
                    "nsfw": item.over_18
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
                    "votes": item.score,
                    "nsfw": item.submission.over_18
                }
                
                saved_items["comments"].append(comment_data)

        final_output = {
            "last_pulled": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            "counts": counts,
            "content": saved_items
        }
        
        elapsed_time = time.time() - start_time
        
        print(f"Completed fetching items in {elapsed_time:.2f} seconds.")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        final_output = {}
    
    # Assuming an average fetch time per post for comments is known or calculated
    average_fetch_time_per_post = 5  # Example average time in seconds
    total_posts = len(saved_items["posts"])
    estimated_time = total_posts * average_fetch_time_per_post / 60  # Convert to minutes
    
    message = (
    f"{BOLD}{YELLOW}Warning: Fetching comments for each post is time-consuming, with each post taking almost {average_fetch_time_per_post} seconds.\n"
    f"You have {total_posts} posts. This may take approximately {estimated_time:.2f} minutes.{RESET}\n"
    "Do you want to fetch top 5 comments for each post? (y/n): ")
    
    user_input = input(message)
    
    if user_input.lower() in ['y', 'yes']:
        start_time = time.time()
        
        total_posts = len(saved_items["posts"])
        for index, post in enumerate(saved_items["posts"], start=1):
            item = reddit.submission(url=post["url"])
            comments = item.comments.list()[:5]  # Adjust the slicing based on your needs
            post["top_comments"] = [
                {
                    "comment_url": f"https://reddit.com{comment.permalink}",
                    "comment_text": comment.body,
                    "datetime": get_readable_datetime(comment.created_utc),
                    "votes": comment.score
                } for comment in comments
            ]
            
            elapsed_time = time.time() - start_time
            posts_remaining = total_posts - index
            estimated_remaining_time = posts_remaining * average_fetch_time_per_post
            
            print(f"Fetched comments for {index}/{total_posts} posts. Elapsed time: {elapsed_time:.2f}s. Estimated remaining time: {estimated_remaining_time:.2f}s.", end='\r', flush=True)
        
        print("Completed fetching comments.")
    
    else:
        print("Skipping fetching comments for posts.")
    
    with open("saved_items.json", "w") as outfile:
        json.dump(final_output, outfile, indent=4)
    
    print("\nFinished processing items.")

if __name__ == "__main__":
    fetch_saved_items()
