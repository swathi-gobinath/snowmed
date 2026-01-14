CREATE OR REPLACE FUNCTION SaveUser(
    p_id BIGINT,
    p_name TEXT,
    p_email TEXT,
    p_password TEXT,
    p_created_at TIMESTAMPTZ DEFAULT NULL,
    p_updated_at TIMESTAMPTZ DEFAULT NULL
)
RETURNS BIGINT AS $$
DECLARE v_id BIGINT;
BEGIN
    INSERT INTO users (
        id, name, email, password, created_at, updated_at
    )
    VALUES (
        p_id, p_name, p_email, p_password, COALESCE(p_created_at, NOW()), COALESCE(p_updated_at, NOW())
    )
    ON CONFLICT (id) DO UPDATE SET
        name = EXCLUDED.name,
        email = EXCLUDED.email,
        password = EXCLUDED.password,
        updated_at = COALESCE(EXCLUDED.updated_at, NOW())
    RETURNING id INTO v_id;

    RETURN v_id;
END;
$$ LANGUAGE plpgsql;
