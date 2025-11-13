up_broker:
	docker-compose -f docker-compose.message-broker.yml up -d

up:
	docker-compose \
    -f docker-compose.services.yml \
    -f docker-compose.api.yml \
    up

down: 
	docker-compose \
    -f docker-compose.message-broker.yml \
    -f docker-compose.services.yml \
    -f docker-compose.api.yml \
    down
