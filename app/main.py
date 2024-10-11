from fastapi import FastAPI
import uvicorn
import os
from .models.Tweet import TweetRequest, TweetRanking, Tweet
from .database.database import vectorial_db

app = FastAPI()

@app.post("/", status_code=201)
async def add_tweets_to_index(request: TweetRequest) -> dict[str, str]:
    request_data = []
    for tweet_data in request.data:
        request_data.append((tweet_data.id, tweet_data.content))
    vectorial_db.add_tweets_to_index(request_data)
    return {"message": "Tweet added to index"}

@app.post("/rank", status_code=201)
async def rank_by_given_tweets(request: TweetRequest) -> dict[str, TweetRanking]:
    tweets_received = []
    for tweet_data in request.data:
        tweets_received.append(tweet_data.content)
    rank_data = vectorial_db.rank_by_tweets_sample(tweets_received)
    tweets_data = [Tweet(id=tweet_id, content=tweet_content) for tweet_id, tweet_content in rank_data.items()]
    return {"ranking": TweetRanking(data=tweets_data)}


if __name__ == "__main__":
    HOST = os.getenv("HOST")
    PORT = int(os.getenv("PORT"))
    uvicorn.run(app, host=HOST, port=PORT, log_level="info", access_log=True)