import praw
from dotenv import load_dotenv
import os

load_dotenv()


class Reddit:
    def __init__(self, client_id=None, client_secret=None, password=None, user_agent=None, username=None):
        if not all([client_id, client_secret]):
            client_id = os.getenv('REDDIT_CLIENT_ID')
            client_secret = os.getenv('REDDIT_CLIENT_SECRET')
            user_agent = os.getenv('REDDIT_USER_AGENT')

        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
        )

    def get_top_posts(self, subreddit_name, limit=10, time_filter='day'):
        subreddit = self.reddit.subreddit(subreddit_name)
        posts = []
        for submission in subreddit.top(time_filter=time_filter, limit=limit):
            posts.append({
                'title': submission.title,
                'selftext': submission.selftext,
                'url': submission.url,
                'score': submission.score,
                'comments': self.get_top_comments(submission)
            })
        return posts

    def get_hot_posts(self, subreddit_name, limit=10):
        subreddit = self.reddit.subreddit(subreddit_name)
        posts = []
        for submission in subreddit.hot(limit=limit):
            posts.append({
                'title': submission.title,
                'selftext': submission.selftext,
                'url': submission.url,
                'score': submission.score,
                'comments': self.get_top_comments(submission)
            })
        return posts

    def search_subreddits(self, query, limit=10):
        subreddits = self.reddit.subreddits.search(query, limit=limit)
        return [
            {'name': subreddit.display_name, 'title': subreddit.title, 'description': subreddit.public_description}
            for subreddit in subreddits
        ]

    @staticmethod
    def get_top_comments(submission, limit=5):
        submission.comments.replace_more(limit=0)
        comments = []
        for comment in submission.comments.list()[:limit]:
            comments.append(comment.body)
        return comments
