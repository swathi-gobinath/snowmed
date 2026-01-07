CREATE OR REPLACE FUNCTION SaveClinicalDocument(
    p_id BIGINT,
    p_dictation_id BIGINT,
    p_hospital_id BIGINT,
    p_department_id BIGINT,
    p_doctor_id BIGINT,
    p_patient_id BIGINT,
    p_encounter_id BIGINT,
    p_document_type TEXT,
    p_version INT,
    p_status TEXT,
    p_final_text TEXT,
    p_fhir_resource_type TEXT,
    p_fhir_json JSONB,
    p_doctor_signature TEXT,
    p_signed_at TIMESTAMPTZ
)
RETURNS BIGINT AS $$
DECLARE v_id BIGINT;
BEGIN
    INSERT INTO clinical_documents (
        dictation_id, hospital_id, department_id, doctor_id,
        patient_id, encounter_id, document_type, version,
        status, final_text, fhir_resource_type, fhir_json,
        doctor_signature, signed_at
    )
    VALUES (
        p_dictation_id, p_hospital_id, p_department_id, p_doctor_id,
        p_patient_id, p_encounter_id, p_document_type, p_version,
        p_status, p_final_text, p_fhir_resource_type, p_fhir_json,
        p_doctor_signature, p_signed_at
    )
    ON CONFLICT (id) DO UPDATE SET
        version = EXCLUDED.version,
        status = EXCLUDED.status,
        final_text = EXCLUDED.final_text,
        fhir_json = EXCLUDED.fhir_json,
        doctor_signature = EXCLUDED.doctor_signature,
        signed_at = EXCLUDED.signed_at,
        updated_at = now()
    RETURNING id INTO v_id;

    RETURN v_id;
END;
$$ LANGUAGE plpgsql;