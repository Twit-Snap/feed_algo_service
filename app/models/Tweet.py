from typing import List
from pydantic import BaseModel

class Tweet(BaseModel):
    id : str
    content: str

    class Config:
        extra = "forbid"
        missing = "forbid"

class TweetRequest(BaseModel):
    data: List[Tweet]
    limit: int

    class Config:
        extra = "forbid"
        missing = "forbid"

class TrendingTopicRequest(BaseModel):
    limit: int

    class Config:
        extra = "forbid"
        missing = "forbid"

class TweetRanking(BaseModel):
    data: List[Tweet]

    class Config:
        extra = "forbid"
        missing = "forbid"

class TrendingTopics(BaseModel):
    data: List[str]

    class Config:
        extra = "forbid"
        missing = "forbid"