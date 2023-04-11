import praw
import openai
from sentiment_analysis import rank_comments_by_emotion
from tqdm import tqdm
from reddit_credentials import CLIENT_SECRET, CLIENT_ID, USERNAME, USER_AGENT, PASSWORD
import time

def generate_responses(subreddit_name, comments_data):
    """Generates responses for the comments_data using OpenAI API"""
    responses = []
    with open('OpenAI_SecretKey.txt') as file:
        openai_key = file.read()

    openai.api_key = openai_key
    for comment_data in tqdm(comments_data):
        comment = comment_data[0]
        user = comment_data[4]
        comment_id = comment_data[3]
        prompt = f'''Write a humorous poem in response to the following comment from '{user}' to cheer them up.
        The theme should be strongly anti-capitalist and anti-imperialist.
        \n\n Comment: "{comment}"
        \n\n Poem:
'''
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=0.9,
            max_tokens=256,
            top_p=1,
            best_of=2,
            frequency_penalty=1.4,
            presence_penalty=0,
            stop=None,
            timeout=15,
        ).choices[0].text.strip()
        response = response.replace(r'\t', '')
        responses.append([comment_id, f'{response}'])
    return responses




def reddit_comment(responses, subreddit):
    # Create a reddit instance
    reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        username=USERNAME,
        password=PASSWORD,
        user_agent=USER_AGENT,
        validate_on_submit=True
    )

    for comment_id, response in responses:

        comment = reddit.comment(id=comment_id)
        comment_response = f'''My electric brain detected anger in your comment. Here's a poem to lift your spirits:
        \n***
        \n\n{response}
        \n***
        \n\n Beep-boop, this was an auto-generated comment.'''
        comment.reply(comment_response)
        # comment = Comment(reddit, id=comment_id)
        # preview = reddit.post_preview(comment_response, subreddit=comment.subreddit.display_name)
        # print(preview)
    print(f'{len(responses)} Comments posted on {subreddit}')


#
# subreddit = 'WorkReform'
# emotion = 'anger'
#
# while True:
#     #gather comments of a particular emotion. Default is the top 5 comments
#     comments_data = rank_comments_by_emotion(subreddit, emotion)[:5]
#
#     print(comments_data)
#
#     #Generate responses using OpenAI text-davinci-003
#     responses = generate_responses(subreddit, comments_data)
#
#     #post replys to reddit
#     reddit_comment(responses)
#
#     #wait for 30 minutes, then run again
#     print('waiting for next loop!')
#     time.sleep(30 * 60)

