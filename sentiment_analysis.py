from transformers import pipeline, set_seed
from comment_collector import comment_collector
import torch

subreddit_name = "WorkReform"

# def get_sadness_score(text):
#     # Load the sentiment analysis pipeline
#     nlp = pipeline("text-classification", model="cardiffnlp/twitter-roberta-base-emotion", tokenizer="cardiffnlp/twitter-roberta-base-emotion")
#
#     # Analyze the sentiment of the text
#     sentiment_analysis = nlp(text)
#
#     # Print the results
#     print(f"Text: {text}")
#     print(f"Sentiment: {sentiment_analysis[0]['label']}")
#     print(f"Confidence: {sentiment_analysis[0]['score']}")


def rank_comments_by_emotion(subreddit_name, emotion):
    # Load sentiment analysis model
    nlp = pipeline("text-classification",
                   model="j-hartmann/emotion-english-distilroberta-base",
                   tokenizer="j-hartmann/emotion-english-distilroberta-base",
                   truncation=True,
                   device=0 if torch.cuda.is_available() else -1)

    # Collect comments from subreddit
    comments = comment_collector(subreddit_name)
    comment_bodies = [comment.body for comment in comments]
    comment_ids = [comment.id for comment in comments]
    comment_users = [comment.author.name if comment.author else None for comment in comments]
    # Generate sentiment analysis for all comments
    print('Analyzing sentiments in comments...')
    set_seed(42)
    sentiments = nlp(comment_bodies)

    # Combine comment bodies, sentiments, and scores into a list of tuples
    ranked_comments = [(comment, sentiment['label'], sentiment['score'], comment_id, comment_user) for comment, sentiment, comment_id, comment_user in zip(comment_bodies, sentiments, comment_ids, comment_users)]

    # Sort comments by emotion and then by score (higher score means stronger emotion)
    ranked_comments.sort(key=lambda x: (x[1] == emotion, x[2]), reverse=True)

    # Filter out comments that do not have the specified emotion label
    ranked_comments = [comment for comment in ranked_comments if comment[1] == emotion and comment[2] >= 0.75]


    print(f'There are {len(ranked_comments)} {emotion} comments in the sample')

    return ranked_comments


# # #available emotions:
# #     anger 🤬
# #     disgust 🤢
# #     fear 😨
# #     joy 😀
# #     neutral 😐
# #     sadness 😭
# #     surprise 😲
#
# ranked_comments = rank_comments_by_emotion(subreddit_name, 'anger')
# for comment in ranked_comments:
#     print(comment)
# # print(ranked_comments)

