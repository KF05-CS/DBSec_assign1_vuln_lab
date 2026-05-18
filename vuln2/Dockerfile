FROM postgres:15

COPY init/init.sql /docker-entrypoint-initdb.d/
COPY init/flag.txt /flag.txt

EXPOSE 5432

