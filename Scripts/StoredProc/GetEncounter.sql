CREATE OR REPLACE FUNCTION GetEncounter(p_id BIGINT DEFAULT NULL)
RETURNS TABLE (
    id BIGINT,
    hospital_id BIGINT,
    patient_id BIGINT,
    doctor_id BIGINT,
    external_id TEXT,
    encounter_type TEXT,
    department_id BIGINT,
    started_at TIMESTAMPTZ,
    ended_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ
) AS $$
BEGIN
    RETURN QUERY
    SELECT e.id, e.hospital_id, e.patient_id, e.doctor_id,
           e.external_id, e.encounter_type, e.department_id,
           e.started_at, e.ended_at, e.created_at
    FROM encounters e
    WHERE p_id IS NULL OR e.id = p_id;
END;
$$ LANGUAGE plpgsql;