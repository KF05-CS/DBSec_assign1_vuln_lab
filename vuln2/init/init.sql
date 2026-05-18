CREATE USER attacker WITH PASSWORD 'attackerpass';

GRANT pg_execute_server_program TO attacker;

CREATE TABLE notes(
    id SERIAL PRIMARY KEY,
    content TEXT
);

INSERT INTO notes(content)
VALUES ('internal company data - vuln2 lab');
