run:
	uvicorn app:app --reload --port 443

dev:
	docker compose -f "docker-compose.dev.yml" -p "api" up --build -d
	make run

build:
	docker compose -f "docker-compose.prod.yml" -p "api" up --build -d

run-production:
	uvicorn app:app --port 4430 --host 0.0.0.0

logs:
	docker logs api


	