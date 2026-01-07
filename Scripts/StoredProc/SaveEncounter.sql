CREATE OR REPLACE FUNCTION SaveEncounter(
    p_id BIGINT,
    p_hospital_id BIGINT,
    p_patient_id BIGINT,
    p_doctor_id BIGINT,
    p_external_id TEXT,
    p_encounter_type TEXT,
    p_department_id BIGINT,
    p_started_at TIMESTAMPTZ,
    p_ended_at TIMESTAMPTZ
)
RETURNS BIGINT AS $$
DECLARE v_id BIGINT;
BEGIN
    INSERT INTO encounters (
        hospital_id, patient_id, doctor_id, external_id,
        encounter_type, department_id, started_at, ended_at
    )
    VALUES (
        p_hospital_id, p_patient_id, p_doctor_id, p_external_id,
        p_encounter_type, p_department_id, p_started_at, p_ended_at
    )
    ON CONFLICT (id) DO UPDATE SET
        doctor_id = EXCLUDED.doctor_id,
        encounter_type = EXCLUDED.encounter_type,
        department_id = EXCLUDED.department_id,
        started_at = EXCLUDED.started_at,
        ended_at = EXCLUDED.ended_at
    RETURNING id INTO v_id;

    RETURN v_id;
END;
$$ LANGUAGE plpgsql;