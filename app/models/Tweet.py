from typing import List, Dict
from pydantic import BaseModel, ConfigDict

class Tweet(BaseModel):
    id : str
    content: str

    model_config = ConfigDict(extra="forbid")

class TweetRequest(BaseModel):
    data: List[Tweet]
    limit: int

    model_config = ConfigDict(extra="forbid")

class TrendingTopicRequest(BaseModel):
    limit: int

    model_config = ConfigDict(extra="forbid")

class TweetRanking(BaseModel):
    data: List[Tweet]

    model_config = ConfigDict(extra="forbid")

class TrendingTopics(BaseModel):
    data: List[Dict[str, int]]

    model_config = ConfigDict(extra="forbid")