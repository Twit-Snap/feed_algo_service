from pydantic import BaseModel, Field

class Tweet(BaseModel):
    id : str
    content: str

    class Config:
        extra = "forbid"
        missing = "forbid"

class TweetRequest(BaseModel):
    data: list[Tweet]

    class Config:
        extra = "forbid"
        missing = "forbid"

class TweetRanking(BaseModel):
    data: list[Tweet]

    class Config:
        extra = "forbid"
        missing = "forbid"