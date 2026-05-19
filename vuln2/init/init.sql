CREATE USER attacker WITH PASSWORD 'attackerpass';

GRANT pg_execute_server_program TO attacker;

GRANT USAGE ON SCHEMA public TO attacker;
GRANT CREATE ON SCHEMA public TO attacker;