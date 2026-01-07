CREATE OR REPLACE FUNCTION SaveDictation(
    p_id BIGINT,
    p_hospital_id BIGINT,
    p_department_id BIGINT,
    p_doctor_id BIGINT,
    p_patient_id BIGINT,
    p_encounter_id BIGINT,
    p_dictation_number TEXT,
    p_language TEXT,
    p_status TEXT,
    p_audio_path TEXT,
    p_duration_sec INT
)
RETURNS BIGINT AS $$
DECLARE v_id BIGINT;
BEGIN
    INSERT INTO dictations (
        hospital_id, department_id, doctor_id, patient_id, encounter_id,
        dictation_number, language, status, audio_path, duration_sec
    )
    VALUES (
        p_hospital_id, p_department_id, p_doctor_id, p_patient_id, p_encounter_id,
        p_dictation_number, p_language, p_status, p_audio_path, p_duration_sec
    )
    ON CONFLICT (dictation_number) DO UPDATE SET
        status = EXCLUDED.status,
        audio_path = EXCLUDED.audio_path,
        duration_sec = EXCLUDED.duration_sec,
        updated_at = now()
    RETURNING id INTO v_id;

    RETURN v_id;
END;
$$ LANGUAGE plpgsql;