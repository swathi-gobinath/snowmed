CREATE OR REPLACE FUNCTION GetDoctor(p_id BIGINT DEFAULT NULL)
RETURNS TABLE (
    id BIGINT,
    hospital_id BIGINT,
    department_id BIGINT,
    abha_professional_id TEXT,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    phone TEXT,
    license_number TEXT,
    specialty TEXT,
    custom_vocab JSONB,
    is_active BOOLEAN,
    created_at TIMESTAMPTZ,
    userid BIGINT,
    photo BYTEA
) AS $$
BEGIN
    RETURN QUERY
    SELECT d.id, d.hospital_id, d.department_id, d.abha_professional_id,
           d.first_name, d.last_name, d.email, d.phone,
           d.license_number, d.specialty, d.custom_vocab,
           d.is_active, d.created_at, d.userid, d.photo
    FROM doctors d
    WHERE p_id IS NULL OR d.id = p_id;
END;
$$ LANGUAGE plpgsql;