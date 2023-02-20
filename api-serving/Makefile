init:
	pip install -U pip
	pip install boto3==1.26.8 mlflow==1.30.0 "fastapi[all]" pandas scikit-learn

app:
	uvicorn app:app --reload

server:
	sudo docker compose up -d

server-clean:
	sudo docker compose down -v
	sudo docker rmi -f api-serving-api-with-model

dependency:
	make -C ../database/ server
	sleep 80
	make -C ../model-registry/ server
	python3 ../model-registry/save_model_to_registry.py

dependency-clean:
	make -C ../model-registry/ server-clean
	make -C ../database/ server-clean

all:
	make dependency
	make server

all-clean:
	make server-clenan
	make dependency-clean