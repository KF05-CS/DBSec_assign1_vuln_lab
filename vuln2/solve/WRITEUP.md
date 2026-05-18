Vuln2 ->  a PostgreSQL privilege escalation vulnerability where a low-privileged database user is able to execute OS commands due to misconfigured permissions. -> granting the attacker account the pg_execute_server_program role, which allows the use of COPY TO PROGRAM. This feature lets PostgreSQL run shell commands turning a database-level account into a path for full command execution inside the Docker container.

Step 1: Prepare the exploit script by making it executable with chmod +x exploit.sh so it can be run directly from the GIT terminal.

Step 2: Execute the exploit using ./exploit.sh. This triggers a PostgreSQL query that abuses COPY TO PROGRAM to run a shell command inside the container.

Step 3: The injected command reads the sensitive file /flag.txt and writes it to /tmp/flag.txt inside the container.

Step 4: Retrieve the result using docker exec -i vuln2-copy-to-program cat /tmp/flag.txt to display the extracted flag.

Step 5: The flag appears in the terminal, confirming successful exploitation.
