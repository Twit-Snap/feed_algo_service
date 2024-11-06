from fastapi import APIRouter
from models.Tweet import TweetRequest, TrendingTopicRequest, TweetRanking, TrendingTopics, Tweet
from controllers.algo_controller import algo_controller
from typing import Dict

router = APIRouter()

@router.post("/", status_code=200)
async def refresh_index_content(request: TweetRequest) -> None:
    algo_controller.add_tweets_to_index(request)

@router.post("/rank", status_code=201)
async def rank_by_given_tweets(request: TweetRequest) -> Dict[str, TweetRanking]:
    search_results = algo_controller.rank_by_given_tweets(request)
    return {"ranking": search_results}

@router.post("/trending", status_code=201)
async def get_trending_topics(request: TrendingTopicRequest) -> Dict[str, TrendingTopics]:
    trending_topics = algo_controller.get_trending_topics(request)
    return {"trends": trending_topics}