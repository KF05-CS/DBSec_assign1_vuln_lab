Vuln2 is a PostgreSQL privilege escalation vulnerability involving COPY TO PROGRAM, where a low-privileged database user can execute OS commands due to misconfigured permissions. The issue occurs when the attacker account is granted the pg_execute_server_program role, enabling PostgreSQL to interact with the underlying operating system through program execution features.

Step 1: Prepare the exploit script by making it executable with chmod +x exploit.sh, allowing it to be run directly from the Git Bash terminal.

Step 2: Execute the exploit using ./exploit.sh. This triggers a PostgreSQL query that abuses COPY TO PROGRAM to execute a shell command inside the container.

Step 3: The injected command reads the sensitive file /flag.txt and redirects its contents into a file on the container filesystem (e.g., /tmp/flag.txt) via a shell command.

Step 4: Retrieve the result using docker exec -i vuln2-copy-to-program cat /tmp/flag.txt, which displays the extracted flag.

Step 5: The flag appears in the terminal, confirming successful exploitation and demonstrating how misconfigured PostgreSQL privileges can lead to operating system command execution inside the container.