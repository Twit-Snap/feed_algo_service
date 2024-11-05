from models.Tweet import TweetRequest, TweetRanking, Tweet
from database.database import vectorial_db


class AlgoController:
    def __init__(self):
        self.__db = vectorial_db

    def add_tweets_to_index(self, request: TweetRequest) -> None:
        request_data = []
        for tweet_data in request.data:
            request_data.append((tweet_data.id, tweet_data.content))

        if len(request_data) > 0:
            self.__db.add_tweets_to_index(request_data)

    def rank_by_given_tweets(self, request: TweetRequest) -> TweetRanking:
        print("Sample in the request: ", request.data)
        print("Limit of the request", request.limit)
        print("Current tweet amount: ", len(self.__db.tweets))

        tweets_received = []
        for tweet_data in request.data:
            tweets_received.append(tweet_data.content)
        limit = request.limit
        rank_data = self.__db.rank_by_tweets_sample(tweets_received, limit)
        tweets_data = [Tweet(id=tweet_id, content=tweet_content)
                       for tweet_id, tweet_content in rank_data.items()]
        return TweetRanking(data=tweets_data)


algo_controller = AlgoController()
