CREATE OR REPLACE FUNCTION SaveDoctor(
    p_id BIGINT,
    p_hospital_id BIGINT,
    p_department_id BIGINT,
    p_abha_professional_id TEXT,
    p_first_name TEXT,
    p_last_name TEXT,
    p_email TEXT,
    p_phone TEXT,
    p_license_number TEXT,
    p_specialty TEXT,
    p_custom_vocab JSONB,
    p_is_active BOOLEAN,
    p_userid BIGINT,
    p_photo BYTEA
)
RETURNS BIGINT AS $$
DECLARE v_id BIGINT;
BEGIN
    INSERT INTO doctors (
        id, hospital_id, department_id, abha_professional_id,
        first_name, last_name, email, phone,
        license_number, specialty, custom_vocab, is_active, userid, photo
    )
    VALUES (
        p_id, p_hospital_id, p_department_id, p_abha_professional_id,
        p_first_name, p_last_name, p_email, p_phone,
        p_license_number, p_specialty, p_custom_vocab, p_is_active, p_userid, p_photo
    )
    ON CONFLICT (id) DO UPDATE SET
        hospital_id = EXCLUDED.hospital_id,
        department_id = EXCLUDED.department_id,
        abha_professional_id = EXCLUDED.abha_professional_id,
        first_name = EXCLUDED.first_name,
        last_name = EXCLUDED.last_name,
        email = EXCLUDED.email,
        phone = EXCLUDED.phone,
        license_number = EXCLUDED.license_number,
        specialty = EXCLUDED.specialty,
        custom_vocab = EXCLUDED.custom_vocab,
        is_active = EXCLUDED.is_active,
        userid = EXCLUDED.userid,
        photo = EXCLUDED.photo
    RETURNING id INTO v_id;

    RETURN v_id;
END;
$$ LANGUAGE plpgsql;