from routers.feed_algorithm import router as algorithm_router
from fastapi import FastAPI
import uvicorn
import os

app = FastAPI(title="Tweet algorithm API",
              description="This is a simple API for providing users with tweets similar to tweets they've interacted recently",
              version="1.0.0")

app.include_router(algorithm_router)

if __name__ == "__main__":
    HOST = os.getenv("HOST")
    PORT = int(os.getenv("PORT"))
    uvicorn.run(app, host=HOST, port=PORT, log_level="info", access_log=True)