init:
	pip install -U pip
	pip install pandas psycopg2-binary scikit-learn

server:
	sudo docker compose up -d

server-clean:
	sudo docker compoes down -v
	sudo docker rmi -f database-data-generator postgres:14.0

db-connection:
	PGPASSWORD=0429 psql -h localhost -p 5432 -U postgres -d postgres