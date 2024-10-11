from fastapi import APIRouter
from models.Tweet import TweetRequest, TweetRanking, Tweet
from controllers.algo_controller import algo_controller
from typing import Dict

router = APIRouter()

@router.post("/", status_code=201)
async def refresh_index_content(request: TweetRequest) -> Dict[str, str]:
    algo_controller.add_tweets_to_index(request)
    return {"message": "Tweet added to index"}

@router.post("/rank", status_code=201)
async def rank_by_given_tweets(request: TweetRequest) -> Dict[str, TweetRanking]:
    search_results = algo_controller.rank_by_given_tweets(request)
    return {"ranking": search_results}