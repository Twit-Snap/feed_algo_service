# feed_algo_service

## Running locally
1. Build the image
```
docker build -t dev-feed-algo .
```
2. Run the image (Memory and CPU limits are optional, but recommended to replicate the deployment environment)
```
docker run --name algo-feed -e HOST=0.0.0.0 -e PORT=8000 -p 8000:8000 --memory=600m --cpus=2 dev-feed-algo
```

## Running the test suite
1. Build the image
```
docker build -t dev-feed-algo .
```
2. Run the image with the env var MODE set on test
```
docker run --name algo-feed -e MODE=test dev-feed-algo
```
