from comment_collector import comment_collector
from sentiment_analysis import rank_comments_by_emotion
from comment_generator import generate_responses, reddit_comment
import time
from datetime import datetime
import tqdm

subreddits = ['WorkReform', 'Hasan_Piker', 'h3h3productions']
emotion = 'anger'


while True:
    for subreddit in subreddits:

        print(f'Looking in {subreddit} for angry posts, please wait')
        # gather comments of a particular emotion. Default is the top 5 comments
        comments_data = rank_comments_by_emotion(subreddit, emotion)[:5]

        print(comments_data)

        # Generate responses using OpenAI text-davinci-003
        responses = generate_responses(subreddit, comments_data)

        # post replys to reddit
        reddit_comment(responses, subreddit)

        # wait for 30 minutes, then run again
        now = datetime.strftime(datetime.now(), '%H:%M:%S')
    print(f'{now} waiting 30 minutes for next loop!')
    time.sleep(30 * 60)
