from routers.feed_algorithm import router as algorithm_router
from fastapi import FastAPI
import uvicorn
import os

import newrelic.agent
newrelic.agent.initialize('newrelic.ini')

app = FastAPI(title="Tweet algorithm API",
              description="This is a simple API for providing users with tweets similar to tweets they've interacted recently",
              version="1.0.0")

@app.middleware("http")
async def add_new_relic_transaction(request, call_next):
    import newrelic.agent
    transaction = newrelic.agent.current_transaction()
    if transaction:
        transaction.name = f"{request.method} {request.url.path}"
    response = await call_next(request)
    return response

app.include_router(algorithm_router)

if __name__ == "__main__":
    HOST = os.getenv("HOST")
    PORT = int(os.getenv("PORT"))
    uvicorn.run(app, host=HOST, port=PORT, log_level="info", access_log=True)