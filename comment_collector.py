import praw
from tqdm import tqdm
import datetime

from reddit_credentials import CLIENT_SECRET, CLIENT_ID, PASSWORD, USER_AGENT, USERNAME

subreddit_name = "AdviceAnimals"

#: create praw instance
reddit = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET,
                     password=PASSWORD,
                     user_agent=USER_AGENT,
                     username=USERNAME)

# Get all the comment ids the user has already replied to in the last day
filtered_ids = []
for comment in reddit.redditor(reddit.user.me().name).comments.new(limit=None):
    if (datetime.datetime.utcnow() - datetime.datetime.utcfromtimestamp(comment.created_utc)).days < 1:
        filtered_ids.append(comment.id)

def comment_collector(subreddit_name):
    subreddit = reddit.subreddit(subreddit_name)

    # Get the 10 newest posts with at least 5 top-level comments
    new_posts = subreddit.new(limit=100)
    relevant_posts = []
    comments = []

    filtered_ids = []
    for comment in reddit.redditor(reddit.user.me().name).comments.new(limit=None):
        if (datetime.datetime.utcnow() - datetime.datetime.utcfromtimestamp(comment.created_utc)).days < 1:
            filtered_ids.append(comment.id)

    for post in new_posts:
        top_level_comments = post.num_comments - post.num_crossposts  # Subtract number of crossposts to get top-level comments
        if top_level_comments >= 5:
            relevant_posts.append(post)

        if len(relevant_posts) == 10:
            break

    print(f'Total posts that meet the criteria: {len(relevant_posts)}')
    top_comments = []
    count = 0
    # Get all the comment ids the user has already replied to in the last day

    for post in tqdm(relevant_posts, desc="Posts processed"):

        # Get the top 10 top-level comments on the post
        comments = post.comments.list()
        comments = [comment for comment in comments if comment.id not in filtered_ids]
        comments_sorted = sorted([c for c in comments if isinstance(c, praw.models.Comment)], key=lambda comment: comment.score, reverse=True)
        top_comments.append(comments_sorted[10:])
        count += len(comments_sorted)
        # print(top_comments)
        # print(f'Number of comments: {count}')
    flattened = [comment for comment_list in top_comments for comment in comment_list]
    print(f'Total Comments Collected: {len(flattened)}')

    filtered_ids = []
    for comment in reddit.redditor(reddit.user.me().name).comments.new(limit=None):
        if (datetime.datetime.utcnow() - datetime.datetime.utcfromtimestamp(comment.created_utc)).days < 1:
            filtered_comment = comment.parent()
            filtered_ids.append(filtered_comment.id)

    filtered_comments = [comment for comment in flattened if comment.id not in filtered_ids]
    return (filtered_comments)

#
# top_comments = comment_collector(subreddit_name)
#
# for comments in top_comments:
#     for comment in comments:
#         print(f'CommentID:{comment.id}({comment.score}) - {comment.body}')
