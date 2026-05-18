FROM postgres:15

COPY init/init.sql /docker-entrypoint-initdb.d/init.sql

ENV POSTGRES_DB=vulndb
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres

EXPOSE 5432