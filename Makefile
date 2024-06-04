include .env

some:
	pause

start: docker-up
stop: docker-down
restart: docker-down docker-up

rebuild: docker-down docker-build docker-up

full-deploy-on-vds: build-prod-full docker-push vds-down-containers-and-remove-images clear_vds_app_folder vds-copy-app-config vds-up-docker-images

# DEV Docker
docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-down-ro:
	docker-compose down --remove-orphans

# --------------  PROD Docker
build-prod-full: prod-build

prod-build:
	docker-compose -f docker-compose-production-build.yaml build

tag-prod-image:
	docker tag ${REGISTRY_ADDRESS}/${IMAGE_NAME_FOR_BOT}:${IMAGE_TAG}

prod-build-up:
	docker-compose -f docker-compose-production-build.yaml up -d --build

prod-down:
	docker-compose -f docker-compose-production-build.yaml down -v --remove-orphans


# ----------------------------------------------

# Poetry
show-poetry:
	docker-compose run bot-app poetry show --tree

# Check code
check-code:
	isort main.py app/
	flake8 --extend-ignore E501,F401 main.py app/

# Deploy
build-production:
	docker build --pull --file=docker/production/bot-app.dockerfile --tag ${REGISTRY_HOST}/${REGISTRY_ADDRESS}/${IMAGE_NAME_FOR_BOT}:${IMAGE_TAG} .

docker-commit:
	docker commit ${REGISTRY_HOST}/${REGISTRY_ADDRESS}/${IMAGE_NAME_FOR_BOT}:${IMAGE_TAG}

docker-push:
	docker push ${REGISTRY_HOST}/${REGISTRY_ADDRESS}/${IMAGE_NAME_FOR_BOT}:${IMAGE_TAG}
	docker push ${REGISTRY_HOST}/${REGISTRY_ADDRESS}/${IMAGE_NAME_FOR_SCHEDULE_APP}:${IMAGE_TAG}

docker-pull:
	docker pull ${REGISTRY_HOST}/${REGISTRY_ADDRESS}/${IMAGE_NAME_FOR_BOT}:${IMAGE_TAG}
	docker pull ${REGISTRY_HOST}/${REGISTRY_ADDRESS}/${IMAGE_NAME_FOR_SCHEDULE_APP}:${IMAGE_TAG}

# ----- install docker on VPS -----
vds-install-docker:
	ssh ${REMOTE_VDS_USER_NAME}@${REMOTE_VDS_IP} 'sudo apt-get update'
	ssh ${REMOTE_VDS_USER_NAME}@${REMOTE_VDS_IP} 'sudo apt-get install ca-certificates curl'
	ssh ${REMOTE_VDS_USER_NAME}@${REMOTE_VDS_IP} 'sudo install -m 0755 -d /etc/apt/keyrings'
	ssh ${REMOTE_VDS_USER_NAME}@${REMOTE_VDS_IP} 'sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc'
	ssh ${REMOTE_VDS_USER_NAME}@${REMOTE_VDS_IP} 'sudo chmod a+r /etc/apt/keyrings/docker.asc'
	ssh ${REMOTE_VDS_USER_NAME}@${REMOTE_VDS_IP} 'sudo apt-get update'
	ssh ${REMOTE_VDS_USER_NAME}@${REMOTE_VDS_IP} 'echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null'
	ssh ${REMOTE_VDS_USER_NAME}@${REMOTE_VDS_IP} 'sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin'

vds-install-make:
	sudo apt-get install build-essential

add-mirror-in-docker:
	ssh ${REMOTE_VDS_USER_NAME}@${REMOTE_VDS_IP} 'echo "{ "registry-mirrors": ["https://mirror.gcr.io", "https://daocloud.io", "https://c.163.com/", "https://registry.docker-cn.com"] }" > /etc/docker/daemon.json'
	ssh ${REMOTE_VDS_USER_NAME}@${REMOTE_VDS_IP} 'systemctl reload docker'
	ssh ${REMOTE_VDS_USER_NAME}@${REMOTE_VDS_IP} 'cat /etc/docker/daemon.json'


# ----- VDS loading section -----

vds-docker-ps:
	ssh ${REMOTE_VDS_USER_NAME}@${REMOTE_VDS_IP} 'docker ps -a'

clear_vds_app_folder:
	ssh ${REMOTE_VDS_USER_NAME}@${REMOTE_VDS_IP} 'rm -rf /app'

ssh-bot:
	ssh ${REMOTE_VDS_USER_NAME}@${REMOTE_VDS_IP}

ssh-registry:
	ssh ${REMOTE_REGISTRY_VDS_USER_NAME}@${REMOTE_REGISTRY_VDS_IP}

vds-copy-app-config:
	ssh ${REMOTE_VDS_USER_NAME}@${REMOTE_VDS_IP} 'mkdir /app -p'
	ssh ${REMOTE_VDS_USER_NAME}@${REMOTE_VDS_IP} 'mkdir /app/data -p'
	ssh ${REMOTE_VDS_USER_NAME}@${REMOTE_VDS_IP} 'mkdir /app/dozzle-data -p'
	scp docker-compose-production-load.yaml ${REMOTE_VDS_USER_NAME}@${REMOTE_VDS_IP}:${REMOTE_VDS_PROJECT_FOLDER}
	scp MakefileForVDS ${REMOTE_VDS_USER_NAME}@${REMOTE_VDS_IP}:${REMOTE_VDS_PROJECT_FOLDER}/Makefile
	scp dozzle-data/users.yml ${REMOTE_VDS_USER_NAME}@${REMOTE_VDS_IP}:${REMOTE_VDS_PROJECT_FOLDER}/dozzle-data/users.yml
	scp .env ${REMOTE_VDS_USER_NAME}@${REMOTE_VDS_IP}:${REMOTE_VDS_PROJECT_FOLDER}/.env
	scp .env.prod ${REMOTE_VDS_USER_NAME}@${REMOTE_VDS_IP}:${REMOTE_VDS_PROJECT_FOLDER}/.env.prod
	ssh ${REMOTE_VDS_USER_NAME}@${REMOTE_VDS_IP} 'cat /app/.env.prod >> /app/.env'
	ssh ${REMOTE_VDS_USER_NAME}@${REMOTE_VDS_IP} 'rm -rf /app/.env.prod'



vds-down-containers-and-remove-images:
#	ssh ${REMOTE_VDS_USER_NAME}@${REMOTE_VDS_IP} "sudo timedatectl set-timezone 'Europe/Moscow'"
	ssh ${REMOTE_VDS_USER_NAME}@${REMOTE_VDS_IP} 'docker-compose -f /app/docker-compose-production-load.yaml down -v --remove-orphans'
	#ssh ${REMOTE_VDS_USER_NAME}@${REMOTE_VDS_IP} "systemctl restart docker"
#	ssh ${REMOTE_VDS_USER_NAME}@${REMOTE_VDS_IP} "docker system prune --force --volumes --all"
#	ssh ${REMOTE_VDS_USER_NAME}@${REMOTE_VDS_IP} "docker network prune --force"

vds-up-docker-images:
	ssh ${REMOTE_VDS_USER_NAME}@${REMOTE_VDS_IP} 'docker pull ${REGISTRY_HOST}/${REGISTRY_ADDRESS}/${IMAGE_NAME_FOR_BOT}:${IMAGE_TAG}'
	ssh ${REMOTE_VDS_USER_NAME}@${REMOTE_VDS_IP} 'docker pull ${REGISTRY_HOST}/${REGISTRY_ADDRESS}/${IMAGE_NAME_FOR_SCHEDULE_APP}:${IMAGE_TAG}'
	ssh ${REMOTE_VDS_USER_NAME}@${REMOTE_VDS_IP} 'docker-compose -f /app/docker-compose-production-load.yaml up -d'

vds-server-up: docker-pull
	docker-compose -f docker-compose-production-load.yaml up -d

vds-server-down:
	docker-compose -f docker-compose-production.yaml down -v --remove-orphans

vds-free-space:
	df -h --total