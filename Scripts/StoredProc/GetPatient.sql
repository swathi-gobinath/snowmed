CREATE OR REPLACE FUNCTION GetPatient(p_id BIGINT DEFAULT NULL)
RETURNS TABLE (
    id BIGINT,
    hospital_id BIGINT,
    external_id TEXT,
    first_name TEXT,
    last_name TEXT,
    date_of_birth DATE,
    sex TEXT,
    created_at TIMESTAMPTZ
) AS $$
BEGIN
    RETURN QUERY
    SELECT p.id, p.hospital_id, p.external_id, p.first_name,
           p.last_name, p.date_of_birth, p.sex, p.created_at
    FROM patients p
    WHERE p_id IS NULL OR p.id = p_id;
END;
$$ LANGUAGE plpgsql;