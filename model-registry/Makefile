init:
	pip install -U pip
	pip install boto3==1.26.8 mlflow==1.30.0 scikit-learn pandas

server:
	sudo docker compose up -d

server-clean:
	sudo docker compose down -v
	sudo docker rmi -f mlflow-server minio/minio

dependency:
	make -C ../database/ server

dependency-clean:
	make -C ../database/ server-clean

all:
	make dependency
	make server

all-clean:
	make server-clean
	make dependency-clean