PORTSMAP := $(shell touch ports.map; cat ports.map;)

build:
	./generate_dockerfile.sh
	docker build -t hosttool-honeypy .

build-no-cache:
	./generate_dockerfile.sh
	docker build --no-cache -t hosttool-honeypy .

build-debian:
	./generate_dockerfile.sh debian
	docker build -t hosttool-honeypy .

build-debian-no-cache:
	./generate_dockerfile.sh debian
	docker build --no-cache -t hosttool-honeypy .

run:
	docker run $(PORTSMAP) --rm -i -t hosttool-honeypy /opt/HoneyPy/Honey.py

run-daemon:
	docker run $(PORTSMAP) -d hosttool-honeypy /opt/HoneyPy/Honey.py -d

clean:
	# WARNING: this removes all docker images.
	docker stop $$(docker ps -a -q)
	docker rm $$(docker ps -a -q)
	docker rmi $$(docker images -f dangling=true -a)