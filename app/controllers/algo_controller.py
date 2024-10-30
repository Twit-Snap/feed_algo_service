from models.Tweet import TweetRequest, TrendingTopicRequest, TweetRanking, TrendingTopics, Tweet
from repository.database import vectorial_db
from repository.topicExtractor import topic_extractor

class AlgoController:
    def __init__(self):
        self.__db = vectorial_db
        self.__topic_extractor = topic_extractor

    def add_tweets_to_index(self, request: TweetRequest) -> None:
        request_data = []
        for tweet_data in request.data:
            request_data.append((tweet_data.id, tweet_data.content))
        self.__db.add_tweets_to_index(request_data)
        self.__topic_extractor.load_twit_content(request_data)

    def rank_by_given_tweets(self, request: TweetRequest) -> TweetRanking:
        print("Sample in the request: ", request.data)
        print("Limit of the request", request.limit)
        print("Current tweet amount: ", len(self.__db.tweets))

        tweets_received = []
        for tweet_data in request.data:
            tweets_received.append(tweet_data.content)
        limit = request.limit
        rank_data = self.__db.rank_by_tweets_sample(tweets_received, limit)
        tweets_data = [Tweet(id=tweet_id, content=tweet_content) for tweet_id, tweet_content in rank_data.items()]
        return TweetRanking(data=tweets_data)

    def get_trending_topics(self, request: TrendingTopicRequest) -> TweetRanking:
        print("Limit of the request", request.limit)
        print("Current tweet amount: ", len(self.__db.tweets))

        trending_topics = self.__topic_extractor.extract_topics(request.limit)
        return TrendingTopics(data=trending_topics)

algo_controller = AlgoController()