CREATE OR REPLACE FUNCTION GetDictation(p_id BIGINT DEFAULT NULL)
RETURNS TABLE (
    id BIGINT,
    hospital_id BIGINT,
    department_id BIGINT,
    doctor_id BIGINT,
    patient_id BIGINT,
    encounter_id BIGINT,
    dictation_number TEXT,
    language TEXT,
    status TEXT,
    audio_path TEXT,
    duration_sec INT,
    created_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ
) AS $$
BEGIN
    RETURN QUERY
    SELECT d.id, d.hospital_id, d.department_id, d.doctor_id,
           d.patient_id, d.encounter_id, d.dictation_number,
           d.language, d.status, d.audio_path, d.duration_sec,
           d.created_at, d.updated_at
    FROM dictations d
    WHERE p_id IS NULL OR d.id = p_id;
END;
$$ LANGUAGE plpgsql;