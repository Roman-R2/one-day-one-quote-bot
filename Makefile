start: docker-up
stop: docker-down
restart: docker-down docker-up

rebuild: docker-down docker-build docker-up

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down --remove-orphans

docker-build:
	docker-compose build

show-poetry:
	docker-compose run bot-app poetry show --tree

check-code:
	isort main.py app/
	flake8 --extend-ignore E501,F401 main.py app/