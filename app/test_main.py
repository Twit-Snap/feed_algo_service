import pytest
from fastapi.testclient import TestClient
from routers.feed_algorithm import router

client = TestClient(router)

# Mock data for testing
MOCK_TWEETS = [
    {"id": "1", "content": "FastAPI is amazing!"},
    {"id": "2", "content": "Python makes life easier."},
    {"id": "3", "content": "APIs simplify data integration."}
]

MOCK_NEW_TWEETS = [
    {"id": "4", "content": "New data has arrived."},
    {"id": "5", "content": "Deleting old tweets works!"}
]

MOCK_TWEETS_FOR_TRENDING = [
    {"id": "6", "content": "FastAPI"},
    {"id": "7", "content": "Python"},
    {"id": "8", "content": "APIs"},
    {"id": "9", "content": "FastAPI"},
    {"id": "10", "content": "Python"},
    {"id": "11", "content": "APIs"},
    {"id": "12", "content": "FastAPI"},
    {"id": "13", "content": "Python"},
    {"id": "14", "content": "APIs"},
    {"id": "15", "content": "FastAPI"},
    {"id": "16", "content": "Python"},
    {"id": "17", "content": "APIs"},
    {"id": "18", "content": "FastAPI"},
    {"id": "19", "content": "Python"},
    {"id": "20", "content": "APIs"},
    {"id": "21", "content": "APIs"}
]

EXPECTED_TTS = [{"fastapi": 5}, {"python": 5}, {"apis": 6}]

LONG_TTS = [
        {"id": "22", "content": "Data"},
        {"id": "23", "content": "Science"},
        {"id": "24", "content": "Machine"},
        {"id": "25", "content": "Learning"},
        {"id": "26", "content": "AI"},
        {"id": "27", "content": "Deep"},
        {"id": "28", "content": "Neural"},
        {"id": "29", "content": "Network"},
        {"id": "30", "content": "Algorithm"},
        {"id": "31", "content": "Model"},
        {"id": "32", "content": "Distinct"},
]


@pytest.fixture
def refresh_index():
    # Refresh the index before running tests
    response = client.post("/", json={"data": [], "limit": 10})
    assert response.status_code == 200

def test_refresh_index():
    response = client.post("/", json={"data": MOCK_TWEETS, "limit": 10})
    assert response.status_code == 200

def test_no_old_tweets_after_posting(refresh_index):
    # Post new tweets
    response = client.post("/", json={"data": MOCK_TWEETS, "limit": 10})
    assert response.status_code == 200

    # Verify only new tweets are present
    response = client.post("/", json={"data": MOCK_NEW_TWEETS, "limit": 10})
    assert response.status_code == 200

    # Verify only new tweets are present
    response = client.post("/rank", json={"data": [], "limit": 10})
    ranked_tweets = response.json()["ranking"]["data"]
    ranked_ids = {tweet["id"] for tweet in ranked_tweets}

    # Only new tweets should be in the database
    expected_ids = {tweet["id"] for tweet in MOCK_NEW_TWEETS}
    assert ranked_ids == expected_ids

def test_rank_by_given_tweets(refresh_index):
    # Post new tweets
    response = client.post("/", json={"data": MOCK_TWEETS, "limit": 10})
    assert response.status_code == 200

    # Request ranking
    request_data = {"data": MOCK_TWEETS, "limit": 3}
    response = client.post("/rank", json=request_data)
    assert response.status_code == 201
    assert "ranking" in response.json()
    ranked_tweets = response.json()["ranking"]["data"]

    # Verify the ranking is as expected
    assert len(ranked_tweets) == 3
    for tweet in ranked_tweets:
        assert tweet["id"] in {t["id"] for t in MOCK_TWEETS}

def test_get_trending_topics(refresh_index):
    # Post mock tweets for trending
    response = client.post("/", json={"data": MOCK_TWEETS_FOR_TRENDING, "limit": 20})
    assert response.status_code == 200

    # Request trending topics
    request_data = {"limit": 3}
    response = client.post("/trending", json=request_data)
    assert response.status_code == 201
    assert "trends" in response.json()
    trending_topics = response.json()["trends"]["data"]

    # Verify the trending topics are as expected
    assert len(trending_topics) == 3
    for topic in trending_topics:
        assert topic in EXPECTED_TTS

def test_get_trending_topics_sorted(refresh_index):
    # Post mock tweets for trending
    response = client.post("/", json={"data": MOCK_TWEETS_FOR_TRENDING, "limit": 20})
    assert response.status_code == 200

    # Request trending topics
    request_data = {"limit": 1}
    response = client.post("/trending", json=request_data)
    assert response.status_code == 201
    assert "trends" in response.json()
    trending_topics = response.json()["trends"]["data"]

    # Verify the trending topics are as expected
    assert len(trending_topics) == 1
    assert trending_topics[0] == EXPECTED_TTS[-1]

def test_get_trending_topics_with_more_topics(refresh_index):
    # Post mock tweets for trending
    response = client.post("/", json={"data": MOCK_TWEETS_FOR_TRENDING + LONG_TTS, "limit": 20})
    assert response.status_code == 200

    # Request trending topics
    request_data = {"limit": 3}
    response = client.post("/trending", json=request_data)
    assert response.status_code == 201
    assert "trends" in response.json()
    trending_topics = response.json()["trends"]["data"]

    # Verify the trending topics are as expected
    assert len(trending_topics) == 3
    for topic in trending_topics:
        assert topic in EXPECTED_TTS

def test_trending_topics_with_no_tweets(refresh_index):
    # Remove all tweets from the database
    request_data = {"limit": 3, "data": []}
    response = client.post("/", json=request_data)
    assert response.status_code == 200

    # Request trending topics
    request_data = {"limit": 5}
    response = client.post("/trending", json=request_data)
    assert "trends" in response.json()
    trending_topics = response.json()["trends"]["data"]
    assert len(trending_topics) == 0
