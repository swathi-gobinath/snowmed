CREATE OR REPLACE FUNCTION GetUser(p_id BIGINT DEFAULT NULL)
RETURNS TABLE (
    id BIGINT,
    name TEXT,
    email TEXT,
    password TEXT,
    created_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ
) AS $$
BEGIN
    RETURN QUERY
    SELECT u.id, u.name, u.email, u.password, u.created_at, u.updated_at
    FROM users u
    WHERE (p_id IS NULL OR p_id = 0 OR u.id = p_id);
END;
$$ LANGUAGE plpgsql;
