build:
	docker build -t dev-feed-algo .

run:
	docker run --name algo-feed -e HOST=0.0.0.0 -e PORT=8000 -p 8000:8000 --memory=600m --cpus=2 dev-feed-algo

stop:
	docker stop algo-feed && docker rm algo-feed

clean:
	docker rmi dev-feed-algo

.PHONY: build run stop clean
