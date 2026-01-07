CREATE OR REPLACE FUNCTION SavePatient(
    p_id BIGINT,
    p_hospital_id BIGINT,
    p_external_id TEXT,
    p_first_name TEXT,
    p_last_name TEXT,
    p_date_of_birth DATE,
    p_sex TEXT
)
RETURNS BIGINT AS $$
DECLARE v_id BIGINT;
BEGIN
    INSERT INTO patients (
        hospital_id, external_id, first_name, last_name, date_of_birth, sex
    )
    VALUES (
        p_hospital_id, p_external_id, p_first_name, p_last_name, p_date_of_birth, p_sex
    )
    ON CONFLICT (id) DO UPDATE SET
        external_id = EXCLUDED.external_id,
        first_name = EXCLUDED.first_name,
        last_name = EXCLUDED.last_name,
        date_of_birth = EXCLUDED.date_of_birth,
        sex = EXCLUDED.sex
    RETURNING id INTO v_id;

    RETURN v_id;
END;
$$ LANGUAGE plpgsql;