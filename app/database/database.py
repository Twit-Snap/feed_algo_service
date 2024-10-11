import faiss
from sentence_transformers import SentenceTransformer

#sentence-transformers/all-MiniLM-L6-v2
#jaimevera1107/all-MiniLM-L6-v2-similarity-es

class VectorialDatabase:
    def __init__(self, model_url : str = "jaimevera1107/all-MiniLM-L6-v2-similarity-es"):
        # Initialize the Tweets and uuid containers.
        # As the vectorial database uses integers for indexing, a copy of the uuids is stored in a dictionary.
        self.uuid_hash = {}
        self.tweets = {}

        #Initialize the model for embedding the tweets and the index for the Vect database.
        self.model = SentenceTransformer(model_url)
        _index = faiss.IndexFlatIP(self.model.encode(["Seed"]).shape[1])
        self.index = faiss.IndexIDMap(_index)

    def add_tweets_to_index(self, tweets_data: list[tuple[str, str]]):
        for tweet_uuid, tweet_content in tweets_data:
            internal_tweet_id = len(self.tweets)
            self.tweets[internal_tweet_id] = tweet_content
            self.uuid_hash[internal_tweet_id] = tweet_uuid
        tweets_embedding = self.model.encode(list(self.tweets.values()))
        self.index.add_with_ids(tweets_embedding, list(self.tweets.keys()))

    def rank_by_tweets_sample(self, tweets_sample: list[str], k: int = 3):
        ranking = {}
        tweets_sample_embedding = self.model.encode(tweets_sample)
        D, I = self.index.search(tweets_sample_embedding, k=k)
        for tweet_id in I[0]:
            tweet_uuid = self.uuid_hash[tweet_id]
            tweet_content = self.tweets[tweet_id]
            ranking[tweet_uuid] = tweet_content
        return ranking


vectorial_db = VectorialDatabase("sentence-transformers/all-MiniLM-L6-v2")