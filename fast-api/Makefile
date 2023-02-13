init:
	pip install -U pip
	pip install "fastapi[all]"

main:
	uvicorn main:app --reload

crud-path:
	uvicorn crud_path:app --reload

crud-query:
	uvicorn crud_query:app --reload

crud-pydantic:
	uvicorn crud_pydantic:app --reload

server:
	sudo docker build -t api-server .
	sudo docker run -d api-server -p 8000:8000 api-server

server-clean:
	sudo docker rm -f api-server
	sudo docker rmi -f api-server